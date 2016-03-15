import numpy as np
import pandas as pd

d = {'joining': pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
     'tutorial': pd.Series([10, 2., 3., 4.], index=['beginner_tutorial', 'b', 'c', 'd'])}

df = pd.DataFrame(d)

