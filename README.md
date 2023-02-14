# ABS Factory

Generate python file based on abstruct class.

For example, if you have below python file in `C:\workspace\your_package\base.py`


```python

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
    def complicate(self, sure:bool=True, times=np.array([datetime.timedelta(days=1)])) -> Tuple[bool, Union[list, pd.DataFrame]]:
        if sure:
            df = pd.DataFrame([])
        else:
            df = []
        return True, df

def foo():
    pass
```

You can create template file by
`python abs_factory -f C:\workspace\your_package\base.py` in your working directory.

```python
import datetime
import pandas as pd

class ABSTemplate(Test):

    def test(self):
        raise Exception('Not Implemented')

    def now(self):
        current_time = datetime.datetime.now()
        return current_time

    def complicate(self, sure: bool=True, times=np.array([datetime.timedelta(days=1)])) -> Tuple[bool, Union[list, pd.DataFrame]]:
        if sure:
            df = pd.DataFrame([])
        else:
            df = []
        return (True, df)
```

## Commandline args

`-f` or `--file` (required): specify file name which has abstruct class.

`-o` or `--out` (optional): specify file name to output. default is {working_directory}/{file_name}_template.py

`-n` or `--name` (optional): specify class name defined in output file. default is ABSTemplate
