import os
import pandas as pd

def pos_file(fileBase):
    data = pd.read_csv(fileBase, sep="\s+", skiprows=9)
    data.columns = ['GPS Week', 'GPST', 'latitude(deg)', 'longitude(deg)', 'height(m)', 'Q', 'ns','sdn(m)', 'sde(m)', 'sdu(m)',
                    'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)','ratio']
    return data
