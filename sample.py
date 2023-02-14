import datetime
import difflib
import math
import os
import random

import numpy
import pandas as pd

from abc import ABCMeta, abstractmethod


class Test(metaclass=ABCMeta):
    @abstractmethod
    def test(self):
        raise Exception("Not Implemented")

    @abstractmethod
    def now(self):
        current_time = datetime.datetime.now()
        return current_time

    @abstractmethod
    def complicate(self, sure: bool = True, times=np.array([datetime.timedelta(days=1)])) -> Tuple[bool, Union[list, pd.DataFrame]]:
        if sure:
            df = pd.DataFrame([])
        else:
            df = []
        return True, df


def foo():
    pass
