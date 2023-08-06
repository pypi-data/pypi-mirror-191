from enum import Enum

class Engine(Enum):
    DNN: str
    DNN_OPENVINO: str
    DNN_CUDA: str
    TENSOR_RT: str
    HAILO_RT: str
    QAIC_RT: str

class Accelerator(Enum):
    DEFAULT: str
    CPU: str
    GPU: str
    MYRIAD: str
    NVIDIA: str
    NVIDIA_FP16: str
    HAILO: str
    QAIC: str
