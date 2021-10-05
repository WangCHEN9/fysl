import pandas as pd
import seaborn as sns
from pathlib import Path

excel_path = Path(r'./data/alorsfaim_82102_-_.xlsx')

df = pd.read_excel(excel_path, sheet_name='data')

print(df)
