import torch
from lmppl import LM

model = LM("facebook/opt-30b", torch_dtype=torch.float16)
