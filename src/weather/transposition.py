import numpy as np
import pandas as pd
import sys

in_ = sys.argv[1]
out_ = sys.argv[2] if len(sys.argv) > 2 else in_

df = pd.read_csv(in_, index_col=0)
df.transpose().to_csv(out_, index=True)