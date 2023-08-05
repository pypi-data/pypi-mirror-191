from models.mae_trans.register_models import *
from joonmyung.utils import isDir
import torch


class JModel():
    def __init__(self, model_name, num_classes, model_path, model_number = 0, ana_type = "timm", device=torch.device("cpu")):
        self.model_path = model_path
        self.device = device
        self.ana_type = ana_type
        self.model_number = model_number
        self.model_name = model_name
        self.num_classes = num_classes

    def getModel(self, epoch):
        model_path = self.model_path.format(epoch)
        if not isDir(model_path): return False

        if self.ana_type == "timm":
            # model = models.__dict__[self.model_name](num_classes=self.num_classes)
            # model.to(self.device)
            # model.eval()
            # return model
            pass

        elif self.ana_type == "2023ICCV":
            if self.model_number == 0: # UNMIX CONVOLUTION
                checkpoint = torch.load(model_path)
                net = checkpoint['net']
                net.to(self.device)
                net.eval()

                net_unmixup = checkpoint['net_unmixup']
                net_unmixup.to(self.device)
                net_unmixup.eval()

                args = checkpoint['args']
                return net, net_unmixup, args
            elif self.model_number == 1: # MAE TRANSFORMER
                from timm import create_model
                checkpoint = torch.load(model_path, map_location='cpu')
                args = checkpoint['args']
                model = create_model(
                    args.model,
                    pretrained=args.pretrained,
                    num_classes=args.nb_classes,
                    drop_rate=args.drop,
                    drop_path_rate=args.drop_path,
                    drop_block_rate=args.drop_block,
                    embed_dim=args.embed_dim,
                    input_size=args.input_size,

                    # 2023CVPR
                    cls_token_num=args.cls_token_num,
                    cls_token_YN=args.cls_token_YN,

                    mixed_ratio=args.mixed_ratio,
                    mae_loss_type=args.mae_loss_type,
                    norm_pix_loss=args.norm_pix_loss,
                    decoder_embed_dim=args.decoder_embed_dim,
                    decoder_num_heads=args.decoder_num_heads,
                    mlp_ratio=args.mlp_ratio,
                    decoder_depth=args.decoder_depth,
                ).to(self.device)
                model.load_state_dict(checkpoint['model'])
                return model, args
            elif self.model_number == 2:
                pass
                # model = preactresnet.__dict__[args.arch](num_classes, args.dropout, per_img_std, stride, drop_block, keep_prob, gamma,
                #                                    patchup_block, unmixup=args.unmixup, train=args.train
                #                                    , p=args.p
                #                                    , mixed_ratio=args.mixed_ratio
                #                                    , mae_loss_type=args.mae_loss_type
                #                                    , norm_pix_loss=args.norm_pix_loss
                #                                    , decoder_embed_dim=args.decoder_embed_dim
                #                                    , decoder_num_heads=args.decoder_num_heads
                #                                    , mlp_ratio=args.mlp_ratio
                #                                    , decoder_depth=args.decoder_depth
                #                                    , norm_layer=nn.LayerNorm
        return False