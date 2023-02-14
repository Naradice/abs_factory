import ast

code = """
import pandas as pd
import numpy as np

from typing import Tuple, Union


class Test:
    @abstractmethod
    def test(self):
        raise Exception("Not Implemented")
    
    @abstractmethod
    def now(self):
        current_time = datetime.datetime.now()
        return current_time
        
    @abstractmethod
    def complicate(self, sure:bool=True, times=np.array([datetime.timedelta(days=1)])) -> Tuple[bool, Union[list, pd.DataFrame]]:
        if sure:
            df = pd.DataFrame([])
        else:
            df = []
        return True, df

def foo():
    pass
"""

code_ast_obj = ast.parse(code)
