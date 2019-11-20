import os
import pandas as pd
import numpy as np
import georinex as gr

def obtain_data(file_path, file_path_nav, file_path_sp3):

  obs = gr.load(file_path)
  obs_df = obs.to_dataframe()

  nav = gr.load(file_path_nav)
  nav_df = nav.to_dataframe()

  sp3 = gr.load(file_path_sp3)
  sp3_df = sp3.to_dataframe()

  return obs_df, nav_df, sp3_df
