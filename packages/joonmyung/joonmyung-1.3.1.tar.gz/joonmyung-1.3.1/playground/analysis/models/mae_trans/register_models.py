# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the CC-by-NC license found in the
# LICENSE file in the root directory of this source tree.
#

import torch
import torch.nn as nn
from functools import partial

from timm.models.vision_transformer import _cfg
from timm.models.registry import register_model
from .deit import VisionTransformer

@register_model
def deit_tiny(pretrained=False, **kwargs):
    num_heads = 3                    # 3 & 64 : DeiT
    kwargs['embed_dim'] *= num_heads # 4 & 48 : ConViT
    model = VisionTransformer(
        num_heads=num_heads,
        norm_layer=partial(nn.LayerNorm, eps=1e-6), **kwargs)
    model.default_cfg = _cfg()
    # if pretrained:
    #     checkpoint = torch.hub.load_state_dict_from_url(
    #         url="https://dl.fbaipublicfiles.com/convit/convit_tiny.pth",
    #         map_location="cpu", check_hash=True
    #     )
    #     model.load_state_dict(checkpoint)

    return model


@register_model
def deit_small(pretrained=False, **kwargs):
    num_heads = 6 # 9 → 6
    kwargs['embed_dim'] *= num_heads # 9개
    model = VisionTransformer(
        num_heads=num_heads,
        norm_layer=partial(nn.LayerNorm, eps=1e-6), **kwargs)
    model.default_cfg = _cfg()
    # if pretrained:
    #     checkpoint = torch.hub.load_state_dict_from_url(
    #         url="https://dl.fbaipublicfiles.com/convit/convit_small.pth",
    #         map_location="cpu", check_hash=True
    #     )
    #     model.load_state_dict(checkpoint)

    return model
