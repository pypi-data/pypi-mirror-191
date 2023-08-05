import os, sys

from joonmyung.utils import to_np

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import matplotlib
import shutil

matplotlib.use('agg')
import matplotlib.pyplot as plt
import random

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

class RecorderMeter(object):
    """Computes and stores the minimum loss value and its epoch index"""

    def __init__(self, total_epoch):
        self.reset(total_epoch)

    def reset(self, total_epoch):
        assert total_epoch > 0
        self.total_epoch = total_epoch
        self.current_epoch = 0
        self.epoch_losses = np.zeros((self.total_epoch, 2), dtype=np.float32)  # [epoch, train/val]
        self.epoch_losses = self.epoch_losses - 1

        self.epoch_accuracy = np.zeros((self.total_epoch, 2), dtype=np.float32)  # [epoch, train/val]
        self.epoch_accuracy = self.epoch_accuracy

    def update(self, idx, train_loss, train_acc, val_loss, val_acc):
        assert idx >= 0 and idx < self.total_epoch, 'total_epoch : {} , but update with the {} index'.format(
            self.total_epoch, idx)
        self.epoch_losses[idx, 0] = train_loss
        self.epoch_losses[idx, 1] = val_loss
        self.epoch_accuracy[idx, 0] = train_acc
        self.epoch_accuracy[idx, 1] = val_acc
        self.current_epoch = idx + 1
        return self.max_accuracy(False) == val_acc

    def max_accuracy(self, istrain):
        if self.current_epoch <= 0: return 0
        if istrain:
            return self.epoch_accuracy[:self.current_epoch, 0].max()
        else:
            return self.epoch_accuracy[:self.current_epoch, 1].max()

    def plot_curve(self, save_path):
        title = 'the accuracy/loss curve of train/val'
        dpi = 80
        width, height = 1200, 800
        legend_fontsize = 10
        scale_distance = 48.8
        figsize = width / float(dpi), height / float(dpi)

        fig = plt.figure(figsize=figsize)
        x_axis = np.array([i for i in range(self.total_epoch)])  # epochs
        y_axis = np.zeros(self.total_epoch)

        plt.xlim(0, self.total_epoch)
        plt.ylim(0, 100)
        interval_y = 5
        interval_x = 5
        plt.xticks(np.arange(0, self.total_epoch + interval_x, interval_x))
        plt.yticks(np.arange(0, 100 + interval_y, interval_y))
        plt.grid()
        plt.title(title, fontsize=20)
        plt.xlabel('the training epoch', fontsize=16)
        plt.ylabel('accuracy', fontsize=16)

        y_axis[:] = self.epoch_accuracy[:, 0]
        plt.plot(x_axis, y_axis, color='g', linestyle='-', label='train-accuracy', lw=2)
        plt.legend(loc=4, fontsize=legend_fontsize)

        y_axis[:] = self.epoch_accuracy[:, 1]
        plt.plot(x_axis, y_axis, color='y', linestyle='-', label='valid-accuracy', lw=2)
        plt.legend(loc=4, fontsize=legend_fontsize)

        y_axis[:] = self.epoch_losses[:, 0]
        plt.plot(x_axis, y_axis * 50, color='g', linestyle=':', label='train-loss-x50', lw=2)
        plt.legend(loc=4, fontsize=legend_fontsize)

        y_axis[:] = self.epoch_losses[:, 1]
        plt.plot(x_axis, y_axis * 50, color='y', linestyle=':', label='valid-loss-x50', lw=2)
        plt.legend(loc=4, fontsize=legend_fontsize)

        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print('---- save figure {} into {}'.format(title, save_path))
        plt.close(fig)


def time_string():
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    string = '[{}]'.format(time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())))
    return string


def convert_secs2time(epoch_time):
    need_hour = int(epoch_time / 3600)
    need_mins = int((epoch_time - 3600 * need_hour) / 60)
    need_secs = int(epoch_time - 3600 * need_hour - 60 * need_mins)
    return need_hour, need_mins, need_secs


def time_file_str():
    ISOTIMEFORMAT = '%Y-%m-%d'
    string = '{}'.format(time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())))
    return string + '-{}'.format(random.randint(1, 10000))


def to_one_hot(inp, num_classes):
    """
    creates a one hot encoding that is a representation of categorical variables as binary vectors for the given label.
    Args:
        inp: label of a sample.
        num_classes: the number of labels or classes that we have in the multi class classification task.

    Returns:
        one hot encoding vector of the specific target.
    """
    y_onehot = torch.FloatTensor(inp.size(0), num_classes)
    y_onehot.zero_()

    y_onehot.scatter_(1, inp.unsqueeze(1).data.cpu(), 1)

    return Variable(y_onehot.to(device), requires_grad=False)


def binary_cross_entropy(inputs, target, weight=None, reduction='mean', smooth_eps=None, from_logits=False):
    """cross entropy loss, with support for label smoothing https://arxiv.org/abs/1512.00567"""
    smooth_eps = smooth_eps or 0
    if smooth_eps > 0:
        target = target.float()
        target.add_(smooth_eps).div_(2.)
    if from_logits:
        return F.binary_cross_entropy_with_logits(inputs, target, weight=weight, reduction=reduction)
    else:
        return F.binary_cross_entropy(inputs, target, weight=weight, reduction=reduction)


def binary_cross_entropy_with_logits(inputs, target, weight=None, reduction='mean', smooth_eps=None, from_logits=True):
    return binary_cross_entropy(inputs, target, weight, reduction, smooth_eps, from_logits)


def accuracy(output, target, topk=(1,)):
    """
    This function computes the top k accuracy for a given predicted labels and the targets.
    Args:
        output: output of the model
        target: truth value or the real target of the samples.
        topk: to define the k value to evaluates the accuracy

    Returns:
        top k accuracy.
    """
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


def to_var(x,requires_grad=True):
    x = x.to(device)
    return Variable(x, requires_grad=requires_grad)


def get_similarity(h1, h2, h_prime):
    """
    This function accepts two hidden representations and also the interpolated hidden representation.
    And calculates the cosine similarity of pair of flattened hidden representations.
    Args:
        h1: CNN hidden representation for the firs sample in the pair.
        h2: CNN hidden representation for the second sample in the pair.
        h_prime: interpolated hidden representation.
    Returns:
        the cosine similarity of the combination pair of the input hidden representations.
    """
    #  create flatten hidden representations
    h1 = h1.view(h1.size(0), -1)
    h2 = h2.view(h2.size(0), -1)
    h_prime = h_prime.view(h_prime.size(0), -1)
    # calculate the cosine similarity similarity.
    sim_1_2 = nn.CosineSimilarity(h1, h2)
    sim_p_1 = nn.CosineSimilarity(h_prime, h1)
    sim_p_2 = nn.CosineSimilarity(h_prime, h2)
    return sim_1_2, sim_p_1, sim_p_2


def copy_script_to_folder(caller_path, folder):
    """
    This function is responsible to make a copy from the running script and save it into the given folder.
    Args:
        caller_path: script that run the experiment and we want to make copy of it and archive it along with the result.
        folder: destination path.
    """
    script_filename = caller_path.split('/')[-1]
    script_relative_path = os.path.join(folder, script_filename)
    # Copying script
    shutil.copy(caller_path, script_relative_path)















import wandb
import PIL
import cv2
def data2PIL(datas, to_numpy=False):
    if type(datas) == torch.Tensor:
        if len(datas.shape) == 3: datas = datas.unsqueeze(0)
        pils = datas.permute(0, 2, 3, 1).detach().cpu()
    elif type(datas) == PIL.JpegImagePlugin.JpegImageFile:
        pils = datas
    elif type(datas) == np.ndarray:
        if len(datas.shape) == 3: datas = np.expand_dims(datas, axis=0)
        if datas.max() <= 1:
            # image = Image.fromarray(image)                 # 0.32ms
            pils = cv2.cvtColor(datas, cv2.COLOR_BGR2RGB)   # 0.29ms
    else:
        raise ValueError
    if to_numpy: pils = to_np(pils)
    return pils


class AverageMeter:
    ''' Computes and stores the average and current value. '''
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.val = 0.0
        self.avg = 0.0
        self.sum = 0.0
        self.count = 0

    def update(self, val: float, n: int = 1) -> None:
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
    # def updateTime(self, val: float): -> None:

    def __str__(self):
        return "\
        end = time.time() \n\
        batch_time = AverageMeter() \n\
        batch_time.update(time.time() - end) \n\
        end = time.time() \n\
        avg_score = AverageMeter()\n\
        accuracy = 0.1\n\
        avg_score.update(accuracy)\n\
        losses = AverageMeter()\n\
        loss = 0\n\
        batch_size = 128\n\
        losses.update(loss.data.item(), batch_size)\n\
        print(f'time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'\n\
              f'loss {losses.val:.4f} ({losses.avg:.4f})\t' \n\
              f'acc {avg_score.val:.4f} ({avg_score.avg:.4f})')"




class Logger():
    loggers = {}
    def __init__(self, use_wandb=True, wandb_entity=None, wandb_project=None, wandb_name=None, wandb_watch=False
                 , args=None, model=False
                 , save=True):
        self.use_wandb = use_wandb
        if use_wandb:
            wandb.init(entity=wandb_entity, project=wandb_project, name=wandb_name, resume="allow",
                       config=args)
            if wandb_watch and model: wandb.watch(model, log='all')
            if save and args: torch.save({'args': args, }, os.path.join(wandb.run.dir, "args.pt"))

    def getLog(self, k, return_type =None):
        if return_type == "avg":
            return self.loggers[k].avg
        elif return_type == "val":
            return self.loggers[k].val
        else:
            return self.loggers[k]

    def delLog(self, columns: list):
        for column in columns:
            self.loggers.pop(column)

    def resetLog(self):
        self.loggers = {k:AverageMeter() if type(v) == AverageMeter else v for k, v in self.loggers.items()}

    def addLog(self, datas:dict, epoch=None, mae_task_type = None, bs = 1):
        for k, v in datas.items():
            data_type = v[0]
            if data_type == 0:  # Values
                self.loggers[k] = v[1]
            elif data_type == 1: # AverageMeter
                if k not in self.loggers.keys():
                    self.loggers[k] = AverageMeter()
                self.loggers[k].update(v[1], bs)
            elif data_type == 2: # Table
                columns = list(v[1].keys())
                data_num = len(list(v[1].values())[0])
                self.loggers[k] = wandb.Table(columns=["epoch", "MTT"] + columns)
                for idx in range(data_num):
                    self.loggers[k].add_data(str(epoch), str(mae_task_type), *[wandb.Image(to_np(data2PIL(v[1][k][idx]))) if len(v[1][k].shape) == 4 else to_np(v[1][k])[idx] for k in columns])
        return True

    def getPath(self):
        return wandb.run.dir

    def logWandb(self):
        if self.use_wandb:
            wandb.log({k:v.avg if type(v) == AverageMeter else v for k, v in self.loggers.items()})
            self.resetLog()
        else:
            print("Wandb is not Working Now")

    def finish(self):
        wandb.finish()

import numpy as np
import torch
def get_2d_sincos_pos_embed(embed_dim, grid_size, cls_token=False):
    grid_h = np.arange(grid_size, dtype=np.float32)
    grid_w = np.arange(grid_size, dtype=np.float32)
    grid = np.meshgrid(grid_w, grid_h)  # here w goes first
    grid = np.stack(grid, axis=0)

    grid = grid.reshape([2, 1, grid_size, grid_size])
    pos_embed = get_2d_sincos_pos_embed_from_grid(embed_dim, grid)
    if cls_token:
        pos_embed = np.concatenate([np.zeros([1, embed_dim]), pos_embed], axis=0)
    return pos_embed


def get_2d_sincos_pos_embed_from_grid(embed_dim, grid):
    assert embed_dim % 2 == 0

    # use half of dimensions to encode grid_h
    emb_h = get_1d_sincos_pos_embed_from_grid(embed_dim // 2, grid[0])  # (H*W, D/2)
    emb_w = get_1d_sincos_pos_embed_from_grid(embed_dim // 2, grid[1])  # (H*W, D/2)

    emb = np.concatenate([emb_h, emb_w], axis=1) # (H*W, D)
    return emb


def get_1d_sincos_pos_embed_from_grid(embed_dim, pos):
    """
    embed_dim: output dimension for each position
    pos: a list of positions to be encoded: size (M,)
    out: (M, D)
    """
    assert embed_dim % 2 == 0
    omega = np.arange(embed_dim // 2, dtype=np.float)
    omega /= embed_dim / 2.
    omega = 1. / 10000**omega  # (D/2,)

    pos = pos.reshape(-1)  # (M,)
    out = np.einsum('m,d->md', pos, omega)  # (M, D/2), outer product

    emb_sin = np.sin(out) # (M, D/2)
    emb_cos = np.cos(out) # (M, D/2)

    emb = np.concatenate([emb_sin, emb_cos], axis=1)  # (M, D)
    return emb

def interpolate_pos_embed(model, checkpoint_model):
    if 'pos_embed' in checkpoint_model:
        pos_embed_checkpoint = checkpoint_model['pos_embed']
        embedding_size = pos_embed_checkpoint.shape[-1]
        num_patches = model.patch_embed.num_patches
        num_extra_tokens = model.pos_embed.shape[-2] - num_patches
        # height (== width) for the checkpoint position embedding
        orig_size = int((pos_embed_checkpoint.shape[-2] - num_extra_tokens) ** 0.5)
        # height (== width) for the new position embedding
        new_size = int(num_patches ** 0.5)
        # class_token and dist_token are kept unchanged
        if orig_size != new_size:
            print("Position interpolate from %dx%d to %dx%d" % (orig_size, orig_size, new_size, new_size))
            extra_tokens = pos_embed_checkpoint[:, :num_extra_tokens]
            # only the position tokens are interpolated
            pos_tokens = pos_embed_checkpoint[:, num_extra_tokens:]
            pos_tokens = pos_tokens.reshape(-1, orig_size, orig_size, embedding_size).permute(0, 3, 1, 2)
            pos_tokens = torch.nn.functional.interpolate(
                pos_tokens, size=(new_size, new_size), mode='bicubic', align_corners=False)
            pos_tokens = pos_tokens.permute(0, 2, 3, 1).flatten(1, 2)
            new_pos_embed = torch.cat((extra_tokens, pos_tokens), dim=1)
            checkpoint_model['pos_embed'] = new_pos_embed
