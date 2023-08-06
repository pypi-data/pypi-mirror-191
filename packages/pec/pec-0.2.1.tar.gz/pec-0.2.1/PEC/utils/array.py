from sklearn.utils import Bunch
from multiprocessing.shared_memory import SharedMemory
import numpy as np

class SharedArray(Bunch):
    def __init__(self, name, shape, dtype):
        super().__init__(name=name, shape=shape, dtype=dtype)

    @staticmethod
    def create(data):
        shm = SharedMemory(create=True, size=data.nbytes)
        X = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
        X[:] = data[:]

        return shm, SharedArray(shm.name, data.shape, data.dtype)

    def open(self):
        shm = SharedMemory(name=self.name)
        X = np.ndarray(self.shape, dtype=self.dtype, buffer=shm.buf)
        return shm, X
