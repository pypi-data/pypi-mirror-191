from enum import Enum


class Device(Enum):
    MPS = 'mps'
    CPU = 'cpu'
    CUDNN = 'cudnn'
    MKL = 'mkl'
    MKLDNN = 'mkldnn'
    OPENMP = 'openmp'
    QUANTIZED = 'quantized'
