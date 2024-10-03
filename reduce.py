import multiprocessing as mp
import numpy as np


class processor(mp.Process):
    def __init__(self, id: int, data: np.ndarray):
        super()
        self.data = data
        self.id = bin(id)[::-1]  # BigEndian

    def get_data(self): return self.data
    def get_id(self): return self.id

    def set_temp(self, temp: float):
        self.temp = temp

    def run(func, *args, **kwargs):
        func(*args, **kwargs)


# def reduce(data: np.ndarray, p: int):
#     for pu in pool:
#         pu.run()
#     for k in range(np.ceil(np.log2(p))):
#         for pu in pool:
#             p = mp.Process(name=i, target=reduce.reduce(), args=(n, i))
#             pu.start()


def reduce_step(pu: processor, n, p):
    x = atomic_reduction(pu.get_data())
    for k in np.ceil(np.log2(p)):
        print(k)
        # if pu.get_id()[k]


def atomic_reduction(data: np.ndarray):
    return sum(data)
