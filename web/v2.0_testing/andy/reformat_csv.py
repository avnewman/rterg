#!/usr/bin/env python3
# Andrew Newman
# last updated Wed Apr 21 15:56:13 EDT 2021


# just reread the pkl and reformat the csv for testing (add url)

import pandas as pd
import glob
import sys
import pickle

with open('rterg_summary.pkl', 'rb') as f:
    df = pickle.load(f)

df2=df[df['Me']>=6.5]
# needs to be modified to add correct address
df['URL']="http://geophysics.eas.gatech.edu/anewman/research/RTerg/2021/21031600/"
df.to_csv('rterg_summary2.csv')
df2.to_csv('rterg_summary_M65.csv')
