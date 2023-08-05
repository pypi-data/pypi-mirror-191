import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import numpy as np
import torch


from timm.models.layers import DropPath, to_2tuple, trunc_normal_

import torch
import torch.nn as nn


class UnMixup(object):
    """Randomly mask out one or more patches from an image.
    The following code was implemented by the authors of cutout paper.
    https://arxiv.org/abs/1708.04552
    following is the the link to the official implementation of cutout.
    https://github.com/uoguelph-mlrg/Cutout/blob/master/util/cutout.py
    Args:
        n_holes (int): Number of patches to cut out of each image.
        length (int): The length (in pixels) of each square patch.
    """

    def __init__(self, input_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        input_size = to_2tuple(input_size)
        patch_size = to_2tuple(patch_size)
        num_patches = (input_size[1] // patch_size[1]) * (input_size[0] // patch_size[0])
        self.input_size = input_size
        self.patch_size = patch_size
        self.num_patches = num_patches

        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
    def __call__(self, img):
        return self.apply(img)

    def apply(self, x):
        B, C, H, W = x.shape
        assert H == self.input_size[0] and W == self.input_size[1], \
            f"Input image size ({H}*{W}) doesn't match model ({self.input_size[0]}*{self.input_size[1]})."
        x = self.proj(x).flatten(2).transpose(1, 2)
        return x
