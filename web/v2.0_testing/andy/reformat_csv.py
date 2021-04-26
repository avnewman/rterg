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

# needs to be modified to add correct address
df['URL']="http://geophysics.eas.gatech.edu/anewman/research/RTerg/2021/21031600/"

df2=df[df['Me']>=6.5]
df.to_csv('rterg_summary2.csv')
df2.to_csv('rterg_summary_M65.csv')


# attempt to write to google sheet
# set up google API auth here: https://pygsheets.readthedocs.io/en/latest/authorization.html
# following connection infomration here https://erikrood.com/Posts/py_gsheets.html
import pygsheets

# authorization
#gc = pygsheets.authorize(service_file='./rterg-cat-c9494a26a4db.json')
# moved out of shared directory as I accidently pushed the old key (needs to remain private)
gc = pygsheets.authorize(service_file='/Users/anewman/Documents/GoogleCloud/keys/rterg-cat-0f0c1afdc799.json')

# open remote google sheet
sh = gc.open('RTerg_cat')  # should match name I assume

wks = sh[0] # first sheet
wks.resize(rows=len(df))  # by default google sheets are only 1000 rows.  Need to resize to allow new data
wks.set_dataframe(df,(0,0))  # write everything to sheet

#wks.update_value('A1',"Eventname") # update individual value

# need to create new sheet first (within googlesheets)
#  too may have troubles the first few times, as you may need to go into the bottom of google
#   sheets to add more lines
sh[1].resize(rows=len(df2))
sh[1].set_dataframe(df2,(0,0))  # write full dataset to second sheet
