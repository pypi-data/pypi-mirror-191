
from typing import List, Union
from pathlib import Path
from io import BytesIO
import torch
import numpy
from PIL import Image
from numpy import ndarray
from torch import Tensor
from torch import device as TorchDevice
from torchvision import transforms
from iv.cirtorch.networks.imageretrievalnet import extract_vectors
from iv.cirtorch.networks.imageretrievalnet import init_network
from iv.cirtorch.networks.imageretrievalnet import ImageRetrievalNet
from iv.schemas import Device


__version__ = '0.0.6'
VERSION = __version__


class ResNet:
    def __init__(self, weight_file: Union[Path, str], device: Union[Device, str] = Device.CPU) -> None:

        assert isinstance(device, (Device, str))
        self.device = TorchDevice(
            device.value if isinstance(device, Device) else device)

        if isinstance(weight_file, Path):
            weight_file = str(weight_file)

        state: dict = torch.load(weight_file)

        state['state_dict']['whiten.weight'] = state['state_dict']['whiten.weight'][0::4, ::]
        state['state_dict']['whiten.bias'] = state['state_dict']['whiten.bias'][0::4]

        net_params = {}
        net_params['whitening'] = state['meta'].get('whitening', False)
        network: ImageRetrievalNet = init_network(net_params)

        network.to(self.device)

        network.load_state_dict(state['state_dict'])

        network.eval()

        _normalize = transforms.Normalize(
            mean=network.meta['mean'],
            std=network.meta['std']
        )
        transform = transforms.Compose([
            transforms.ToTensor(),
            _normalize
        ])

        self.network = network
        self.transform = transform

    def gen_vector(self, image: Union[Image.Image, ndarray, Path, str, bytes]) -> List[float]:
        if isinstance(image, bytes):
            image_file_like = BytesIO(image)
            _image = Image.open(image_file_like).convert('RGB')
            image = numpy.array(_image)

        if isinstance(image, Image.Image):
            image = image.convert('RGB')
            image = numpy.array(image)

        if isinstance(image, Path) or isinstance(image, str):
            _image = Image.open(str(image)).convert('RGB')
            image = numpy.array(_image)

        assert isinstance(image, ndarray)

        vecs: Tensor = extract_vectors(
            self.network, [image], 512, self.transform, self.device)

        # vecs.cpu().numpy().T

        vector: ndarray = vecs.numpy().T

        return vector[0].tolist()


def l2(vector1: List[float], vector2: List[float]) -> float:
    vector1 = numpy.array(vector1)
    vector2 = numpy.array(vector2)
    return float(numpy.sqrt(numpy.sum(numpy.square(vector1 - vector2))))
