### dropout has been removed in this code. original code had dropout#####
## https://github.com/kuangliu/pytorch-cifar/blob/master/models/resnet.py
'''ResNet in PyTorch.
For Pre-activation ResNet, see 'preact_resnet.py'.
Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385
'''
import os, sys



# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from modules.patchup import PatchUp, PatchUpMode
from modules.drop_block import DropBlock
from utility.utils import to_one_hot
from utility.utils import get_2d_sincos_pos_embed
from modules.mixup import mixup_process, get_lambda
from modules.cutmix import CutMix
from data_loader import per_image_standardization
from timm.models.vision_transformer import PatchEmbed, Block
import random
from einops import rearrange

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

class PreActBlock(nn.Module):
    '''Pre-activation version of the BasicBlock.'''
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(PreActBlock, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)

        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False)
            )

    def forward(self, x):
        out = F.relu(self.bn1(x))
        shortcut = self.shortcut(out) if hasattr(self, 'shortcut') else x
        out = self.conv1(out)
        out = self.conv2(F.relu(self.bn2(out)))
        out += shortcut
        return out


class PreActBottleneck(nn.Module):
    '''Pre-activation version of the original Bottleneck module.'''
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(PreActBottleneck, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion*planes, kernel_size=1, bias=False)

        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False)
            )

    def forward(self, x):
        out = F.relu(self.bn1(x))
        shortcut = self.shortcut(out) if hasattr(self, 'shortcut') else x
        out = self.conv1(out)
        out = self.conv2(F.relu(self.bn2(out)))
        out = self.conv3(F.relu(self.bn3(out)))
        out += shortcut
        return out


class PreActResNet(nn.Module):
    """
    In this implementation PreActResNet consist of a Convolutional module followed
    by 4 residual blocks and a fully connected layer for classification.
    """
    def __init__(self, block, num_blocks, initial_channels, num_classes, per_img_std= False, stride=1, drop_block=7,
                 keep_prob=.9, gamma=.9, patchup_block=7,
                 **kwargs):
        super(PreActResNet, self).__init__()
        self.in_planes = initial_channels
        self.num_classes = num_classes
        self.per_img_std = per_img_std
        self.keep_prob = keep_prob
        self.gamma = gamma
        self.patchup_block = patchup_block
        self.dropblock = DropBlock(block_size=drop_block, keep_prob=keep_prob)
        self.conv1 = nn.Conv2d(3, initial_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.patchup_0 = PatchUp(block_size=self.patchup_block, gamma=self.gamma)
        self.layer1 = self._make_layer(block, initial_channels, num_blocks[0], stride=1)
        self.patchup_1 = PatchUp(block_size=self.patchup_block, gamma=self.gamma)
        self.layer2 = self._make_layer(block, initial_channels*2, num_blocks[1], stride=2)
        self.patchup_2 = PatchUp(block_size=5, gamma=self.gamma)
        self.layer3 = self._make_layer(block, initial_channels*4, num_blocks[2], stride=2)
        self.patchup_3 = PatchUp(block_size=3, gamma=self.gamma)
        self.layer4 = self._make_layer(block, initial_channels*8, num_blocks[3], stride=2)
        self.patchup_4 = PatchUp(block_size=3, gamma=self.gamma)
        self.linear = nn.Linear(initial_channels*8*block.expansion, num_classes)

        #     2023ICML
        self.p             = kwargs["p"]
        self.train_set     = kwargs["train"]
        self.unmixup       = kwargs["unmixup"]
        self.mixed_ratio   = kwargs["mixed_ratio"]
        self.norm_pix_loss = kwargs["norm_pix_loss"]
        self.mae_loss_type = kwargs["mae_loss_type"]
        self.patch_num     = 16

        decoder_embed_dim = kwargs["decoder_embed_dim"] # 512
        decoder_num_heads = kwargs["decoder_num_heads"] # 4
        mlp_ratio         = kwargs["mlp_ratio"]                 # 0.5
        decoder_depth     = kwargs["decoder_depth"]         # 1
        norm_layer        = kwargs["norm_layer"]         # 1

        self.cls_token  = nn.Parameter(torch.zeros(1, 1, decoder_embed_dim))
        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_embed_dim))
        self.decoder_embed     = nn.Linear(initial_channels*8, decoder_embed_dim, bias=True)
        self.decoder_pos_embed = nn.Parameter(torch.zeros(1, self.patch_num + 1, decoder_embed_dim), requires_grad=False)


        self.decoder_blocks = nn.ModuleList([
            Block(decoder_embed_dim, decoder_num_heads, mlp_ratio, qkv_bias=True, norm_layer=norm_layer)
            for _ in range(decoder_depth)])
        self.decoder_norm = norm_layer(decoder_embed_dim)
        self.decoder_pred = nn.Linear(decoder_embed_dim, self.p ** 2 * 3, bias=True)  # decoder to patch

        self.initialize_weights()

    def initialize_weights(self):
        decoder_pos_embed = get_2d_sincos_pos_embed(self.decoder_pos_embed.shape[-1], int(self.patch_num ** .5), cls_token=True)
        self.decoder_pos_embed.data.copy_(torch.from_numpy(decoder_pos_embed).float().unsqueeze(0))

        # timm's trunc_normal_(std=.02) is effectively normal_(std=0.02) as cutoff is too big (2.)
        torch.nn.init.normal_(self.cls_token, std=.02)
        torch.nn.init.normal_(self.mask_token, std=.02)

        # initialize nn.Linear and nn.LayerNorm
        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            # we use xavier_uniform following official JAX ViT:
            torch.nn.init.xavier_uniform_(m.weight)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def compute_h1(self,x):
        out = x
        out = self.conv1(out)
        out = self.layer1(out)
        return out

    def compute_h2(self,x):
        out = x
        out = self.conv1(out)
        out = self.layer1(out)
        out = self.layer2(out)
        return out

    def get_layer_mix_lam(self, lam, lam_selection, max_rank_glb, k):
        lam_value = None

        if type(lam) == type(None):
            layer_mix = random.randint(1, k)
        else:
            if max_rank_glb:
                data, layer_mix = torch.max(lam[0][:k], 0)
            else:
                data, layer_mix = torch.min(lam[0][:k], 0)

            layer_mix = layer_mix.item() + 1

            if lam_selection:
                lam_value = data
                lam_value = torch.from_numpy(np.array([lam_value]).astype('float32')).to(device)
                lam_value = Variable(lam_value)
        return lam_value, layer_mix

    def forward_encoder(self, x, target= None, mixup=False, manifold_mixup=False, alpha=None,
                lam=None, patchup=False, dropblock=False, epoch=None, patchup_type=PatchUpMode.SOFT, k=2, dropblock_all=False):
        target_a, target_b, target_reweighted, portion = None, None, None, None

        if self.per_img_std:
            x = per_image_standardization(x)

        lam_value = None

        if manifold_mixup or patchup:
            layer_mix = random.randint(0, k)
        elif dropblock and not dropblock_all:
            layer_mix = random.randint(1, k)
        elif mixup:
            layer_mix = 0
        else:
            layer_mix = None

        out = x

        if alpha is not None and type(lam_value) == type(None):
            lam_value = get_lambda(alpha)
            lam_value = torch.from_numpy(np.array([lam_value]).astype('float32')).to(device)
            lam_value = Variable(lam_value)

        if target is not None:
            target_reweighted = to_one_hot(target, self.num_classes)

        if layer_mix == 0 and patchup:
            cutmix = CutMix(beta=1.)
            target_a, target_b, out_m, portion = cutmix.apply(inputs=out, target=target)
            target_a = to_one_hot(target_a, self.num_classes)
            target_b = to_one_hot(target_b, self.num_classes)

            target_reweighted_c = target_a
            target_reweighted_m = portion * target_a + (1.0 - portion) * target_b

            out = torch.cat((out_m, out), dim=0) if self.unmixup > 0 else out_m
            target_reweighted = torch.cat((target_reweighted_m, target_reweighted_c), dim=0) if self.unmixup > 0 else target_reweighted_m

        elif layer_mix == 0 and not patchup:
            out_m, target_reweighted_m = mixup_process(out, target_reweighted, lam=lam_value)

            out = torch.cat((out, out_m), dim=0) if self.unmixup > 0 else out_m
            target_reweighted = torch.cat((target_reweighted, target_reweighted_m), dim=0) if self.unmixup > 0 else target_reweighted_m




        out = self.conv1(out) # (100, 3, 32, 32) → (100, 64, 32, 32)

        if not patchup and not dropblock and (layer_mix == 1 and layer_mix <= k):
            out, target_reweighted = mixup_process(out, target_reweighted, lam=lam_value)
        elif patchup and (layer_mix == 1 and layer_mix <= k):
            target_a, target_b, target_reweighted, out, portion = self.patchup_0(out, target_reweighted, lam=lam_value,
                                                                                 patchup_type=patchup_type)

        if (dropblock and dropblock_all and 1 <= k) or (dropblock and layer_mix == 1 and layer_mix <= k):
            out = self.dropblock(out)

        out = self.layer1(out) # (100, 64, 32, 32) → (100, 64, 32, 32)

        if not patchup and not dropblock and layer_mix == 2 and layer_mix <= k:
            out, target_reweighted = mixup_process(out, target_reweighted, lam=lam_value)
        elif patchup and layer_mix == 2 and layer_mix <= k:
            target_a, target_b, target_reweighted, out, portion = self.patchup_0(out, target_reweighted, lam=lam_value,
                                                                                 patchup_type=patchup_type)
        if (dropblock and dropblock_all and 2 <= k) or (dropblock and layer_mix == 2 and layer_mix <= k):
            out = self.dropblock(out)

        out = self.layer2(out) # (100, 64, 32, 32) → (100, 128, 16, 16)

        if not patchup and not dropblock and layer_mix == 3 and layer_mix <= k:
            out, target_reweighted = mixup_process(out, target_reweighted, lam=lam_value)
        elif patchup and layer_mix == 3 and layer_mix <= k:
            target_a, target_b, target_reweighted, out, portion = self.patchup_0(out, target_reweighted, lam=lam_value,
                                                                                 patchup_type=patchup_type)

        if (dropblock and dropblock_all and 3 <= k) or (dropblock and layer_mix == 3 and layer_mix <= k):
            out = self.dropblock(out)

        out = self.layer3(out) # (100, 128, 16, 16)  → (100, 256, 8, 8)

        if not patchup and not dropblock and layer_mix == 4 and layer_mix <= k:
            out, target_reweighted = mixup_process(out, target_reweighted, lam=lam_value)
        elif patchup and layer_mix == 4 and layer_mix <= k:
            target_a, target_b, target_reweighted, out, portion = self.patchup_0(out, target_reweighted, lam=lam_value,
                                                                                 patchup_type=patchup_type)

        if (dropblock and dropblock_all and 4 <= k) or (dropblock and layer_mix == 4 and layer_mix <= k):
            out = self.dropblock(out)

        out = self.layer4(out) # (100, 256, 8, 8) → (100, 512, 4, 4)
        out_ = out
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)

        return out, out_, target_a, target_b, target_reweighted, lam_value, portion









    def patchify(self, imgs):
        return rearrange(imgs, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=self.p, p2=self.p)

    def unpatchify(self, imgs):
        h = w = int(imgs.shape[1] ** .5)
        return rearrange(imgs, 'b (h w) (p1 p2 c) -> b c (h p1) (w p2)', w=w, p1=self.p, c=3)
    def masking(self, imgs):
        B, C, H, W = imgs.shape  # (100, 3, 32, 32)
        imgs_patch = self.patchify(imgs)
        _, T, D = imgs_patch.shape

        T_mixup = int(T * self.mixed_ratio)
        mask = torch.zeros(B, T, device="cuda").scatter_(1, torch.topk(torch.randn(B, T, device="cuda"), T_mixup, dim=1)[1], 1) # (100(B), 16(T))
        mask_mixup = mask.unsqueeze(dim=-1) # 1 : On(Original) | 0 : Off(Mixed)

        indices = torch.randperm(B, device="cuda")
        imgs_patch = mask_mixup * imgs_patch + (1 - mask_mixup) * imgs_patch[indices]
        x = self.unpatchify(imgs_patch)
        return x, imgs, mask, indices

    def forward_decoder(self, x, mask):
        x = rearrange(x, 'b d p1 p2 -> b (p1 p2) d') # (100(B), 16(T), 512(D))
        B, T, D = x.shape

        mask_tokens = self.mask_token.expand(B, T, -1)
        mask = mask.unsqueeze(-1)
        x = torch.cat([mask * x + (1-mask) * mask_tokens, (1 - mask) * x + mask * mask_tokens]) # (200(B*2), 16(T), 512(D))
        x = self.decoder_embed(x) # (200(B*2), 16(T), 512(D))
        x = torch.cat([self.cls_token.expand(B*2, -1, -1), x], dim=1)

        x = x + self.decoder_pos_embed

        for blk in self.decoder_blocks:
            x = blk(x)
        x = self.decoder_norm(x)

        # predictor projection
        x = self.decoder_pred(x) # (200(B*2), 16(T), 512(D))
        x = x[:, 1:]
        return x # (200(B * 2), 16(T), 192(D))

    def forward_loss(self, imgs, pred, mask, indices):
        B, C, H, W = imgs.shape
        target = self.patchify(imgs)
        if self.norm_pix_loss:
            mean = target.mean(dim=-1, keepdim=True)
            var = target.var(dim=-1, keepdim=True)
            target = (target - mean) / (var + 1.e-6)**.5

        # (B, T, D) → (1)
        if self.mae_loss_type == 0:
            loss_p = (((pred[:B] - target) ** 2).mean(dim=(0,2)) * (1-mask)).sum() / (1-mask).sum()
            loss_n = (((pred[B:] - target[indices]) ** 2).mean(dim=(0,2)) * mask).sum() / mask.sum()
        elif self.mae_loss_type == 1:
            loss_p = ((pred[:B] - target) ** 2).mean()
            loss_n = ((pred[B:] - target[indices]) ** 2).mean()
        else:
            raise ValueError

        return loss_p, loss_n, self.unpatchify(target), self.unpatchify(pred[:B]), self.unpatchify(pred[B:])

    def forward(self, x, target= None, mixup=False, manifold_mixup=False, alpha=None,
                lam=None, patchup=False, dropblock=False, epoch=None, patchup_type=PatchUpMode.SOFT, k=2, dropblock_all=False):
        mae_target, mae_pred_p, mae_pred_n = None, None, None

        if self.train_set == "unmixup" and self.training:
            x, imgs, mask, indices = self.masking(x)
            x_ = x
            out, latent, target_a, target_b, target_reweighted, lam_value, portion = self.forward_encoder(x, target=target, mixup=mixup, manifold_mixup=manifold_mixup, alpha=alpha, lam=lam, patchup=patchup, dropblock=dropblock, epoch=epoch, patchup_type=patchup_type, k=k, dropblock_all=dropblock_all)
            pred     = self.forward_decoder(latent, mask)
            loss_mae_p, loss_mae_n, mae_target, mae_pred_p, mae_pred_n = self.forward_loss(imgs, pred, mask, indices)
        else:
            loss_mae_p, loss_mae_n = 0, 0
            out, latent, target_a, target_b, target_reweighted, lam_value, portion = self.forward_encoder(x, target=target, mixup=mixup, manifold_mixup=manifold_mixup, alpha=alpha, lam=lam, patchup=patchup, dropblock=dropblock, epoch=epoch, patchup_type=patchup_type, k=k, dropblock_all=dropblock_all)

        if self.training:
            return out, target_a, target_b, target_reweighted, lam_value, portion, loss_mae_p, loss_mae_n, mae_target, x_, mae_pred_p, mae_pred_n, indices
        else:
            return out


def preactresnet18(num_classes=10, dropout = False, per_img_std = False, stride=1, drop_block=7, keep_prob=.9,
                   gamma=.9, patchup_block=7, patchup_prob=.7,
                   **kwargs):
    return PreActResNet(PreActBlock, [2,2,2,2], 64, num_classes, per_img_std, stride= stride, drop_block=drop_block,
                        keep_prob=keep_prob, gamma=gamma, patchup_block=patchup_block, **kwargs)

def preactresnet34(num_classes=10, dropout = False, per_img_std = False, stride=1, drop_block=7, keep_prob=.9, gamma=.9,
                   patchup_block=7, patchup_prob=.7,
                   **kwargs):
    return PreActResNet(PreActBlock, [3,4,6,3], 64, num_classes, per_img_std, stride= stride, drop_block=drop_block,
                        keep_prob=keep_prob, gamma=gamma, patchup_block=patchup_block, **kwargs)
