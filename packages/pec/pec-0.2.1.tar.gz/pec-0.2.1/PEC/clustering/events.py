import time

from sklearn.utils import Bunch


class Event(Bunch):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)


class IterationResultEvent(Event):
    def __init__(self, timestamp=None, run_id=None, iteration=None, is_last=None, **kwargs):
        super().__init__(
            "IterationResultEvent",
            timestamp=timestamp,
            run_id=run_id,
            iteration=iteration,
            is_last=is_last,
            **kwargs
        )


class Ack(Event):
    def __init__(self):
        super().__init__(
            "AckEvent",
            timestamp=time.time()
        )
