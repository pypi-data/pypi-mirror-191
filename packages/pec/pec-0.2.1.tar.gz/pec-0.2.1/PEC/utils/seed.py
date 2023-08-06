import numpy as np
from sklearn.utils import check_random_state


class RandomStateGenerator:
    def __init__(self, random_state=None):
        self.random_state = random_state

    def get(self, size=1):
        return check_random_state(self.random_state).randint(np.iinfo(np.int32).max, size=size)
