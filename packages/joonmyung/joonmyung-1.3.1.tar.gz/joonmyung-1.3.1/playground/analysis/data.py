import torch.nn.functional as F
import pandas as pd
import numpy as np
import torch

def makeSample(shape, min=None, max=None, dataType=int, outputType=np, columns=None):
    if dataType == int:
        d = np.random.randint(min, max, size=shape)
    elif dataType == float:
        d = np.random.uniform(low=min, high=max, size=shape)
    else:
        raise ValueError

    if outputType == np:
        return d
    elif outputType == pd:
        return pd.DataFrame(d, columns=None)
    elif outputType == torch:
        return torch.from_numpy(d)


def makeAttn(shape, dim=1):
    return F.softmax(torch.randn(shape), dim=dim)


