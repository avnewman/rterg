#!/usr/bin/env python3
# Chelsea Yangnouvong and Andrew Newman
# last updated Mon Mar  8 10:29:23 EST 2021

import pandas as pd
import glob
import sys

def printerror(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def parseRtergHtml(html):
    colNames1 = ["Eventname", "oDate", "oTime", "Lat.", "Long.", "Depth", "Me", "Txo",
                 "Ehf", "Ebb", "Mehf", "Ehf/Tr^3", "Nstats", "colon", "SRC", "iMag"]
    try:
        df1 = pd.read_csv(html, names = colNames1, skiprows = 1, nrows = 1, delim_whitespace=True)
        df1["Eventname"] = str(int(df1["Eventname"])).zfill(8)   # convert to string with leading zeros
        df1["SRC"] = df1.iloc[0]["SRC"][5:7]
        iMagTypeVal = df1.iloc[0]["iMag"].split("=")[0]
        df1.insert(14, "iMagType", iMagTypeVal)
        df1["iMag"] = df1.iloc[0]["iMag"].split("=")[1][:-2]
        oTimeVal = df1["oDate"] + " " + df1["oTime"]
        df1["oTime"] = pd.to_datetime(oTimeVal, utc=True)
        intSkip1 = 0
    except:
        df1 = pd.DataFrame(columns = colNames1)
        intSkip1 = 1
    
    del df1["colon"]
    del df1["oDate"]
    
    colNames2 = ["TACER_HF", "TACER_BB"]
    
    try:
        df2 = pd.read_csv(html, names = colNames2, skiprows = 2, nrows = 1, delim_whitespace=True, usecols=[7,10])
        float(df2["TACER_HF"][0]) # test to see if there is a valid number
        intSkip2 = 0
    except:
        df2 = pd.DataFrame(columns = colNames2)
        intSkip2 = 1

    colNames3 = ["junk", "Comment"]
    colNames4 = ["junk", "mTime"]
    colNames5 = ["junk", "iteration"]
    
    df3 = pd.read_csv(html, names = colNames3, skiprows = 3 - intSkip2 - intSkip1, nrows = 1, engine="python", delimiter="S:")
    del df3["junk"]
    
    f = open(html, "r")
    content = f.read().split("\n")
    count = -1
    for lines in content:
        count += 1
    if content[count] == "":
        count -= 1
    
    df4 = pd.read_csv(html, names = colNames4, skiprows = count - 1, nrows = 1, delimiter="|")
    if df4["junk"][0][-5:-1] == "</a>":
        del df4["junk"]
    else:
        del df4["mTime"]
        df4.rename(columns = {"junk" : "mTime"}, inplace=True)
    df4["mTime"] = pd.to_datetime(df4["mTime"], utc=True)
    
    df5 = pd.read_csv(html, names = colNames5, skiprows = count, nrows = 1, delimiter="=")
    del df5["junk"]
    df5["iteration"][0] = df5.iloc[0]["iteration"].split("<")[0]

    df = pd.concat([df1,df2,df3,df4, df5], axis=1)
    return df


def builddf(htmlfiles):
    df= pd.DataFrame()
    for html in htmlfiles:
        try: 
            df1=parseRtergHtml(html)
            if len(df) == 0:  # first run keeps header
                df=df1
            else:  # otherwise strip it
                df=df.append(df1, ignore_index = True)               
        except:
            printerror("Skipped",  html, "parseRtergHtml failed to read", sep=" : ")
            continue
    return df

# local testing
#goodfiles=glob.glob('rterg_html_outs/*.html')
#badfiles=glob.glob('rterg_html_outs/bad/*.html')
#htmlfiles = goodfiles + badfiles
# one year 
#  htmlfiles=glob.glob('../../../../events/2021/????????/[0-9]???????.html')
# adding files
#  htmlfiles.append('../../../../events/2018/18101000/18101000.html')
# the below one seems to work now
htmlfiles=sorted(glob.glob('../../../../events/????/????????/[0-9]???????.html'))

df = builddf(htmlfiles)
print(df.head())
print(df.tail())
print(df.index)

df.to_csv('rterg_summary.csv', sep='\t')
df.to_pickle('rterg_summary.pkl')

exit(0)

"""
# OLD
def parseRtergHtml(html):
    colNames1 = ["Eventname", "oDate", "oTime", "Lat.", "Long.", "Depth", "Me", "Txo",
                 "Ehf", "Ebb", "Mehf", "Ehf/Tr^3", "Nstats", "colon", "SRC", "iMag"]
    df1 = pd.read_csv(html, names = colNames1, skiprows = 1, nrows = 1, delim_whitespace=True)
    del df1["colon"]  #remove colon column
    df1["Eventname"] = str(int(df1["Eventname"])).zfill(8)   # convert to string with leading zeros
    df1["SRC"] = df1.iloc[0]["SRC"][5:7]
    iMagTypeVal = df1.iloc[0]["iMag"].split("=")[0]
    df1.insert(14, "iMagType", iMagTypeVal)
    df1["iMag"] = df1.iloc[0]["iMag"].split("=")[1][:-2]
    oTimeVal = df1["oDate"] + " " + df1["oTime"]
    del df1["oDate"]
    df1["oTime"] = pd.to_datetime(oTimeVal, utc=True)
    
    colNames2 = ["TACER_HF", "TACER_BB"]
    try:
        df2 = pd.read_csv(html, names = colNames2, skiprows = 2, nrows = 1, delim_whitespace=True, usecols=[7,10])
        intSkip = 0
        intSkipCol = 0
    except:
        df2 = pd.DataFrame(columns = colNames2)
        intSkip = 2
        intSkipCol = 1
    
    colNames3 = ["junk", "Comment"]
    colNames4 = ["mTime"]
    colNames5 = ["junk", "iteration"]
    skip = 8
    skipCol = 3
    
    df3 = pd.read_csv(html, names = colNames3, skiprows = skipCol - intSkipCol, nrows = 1, delimiter=":")
    del df3["junk"]
    
    df4 = pd.read_csv(html, names = colNames4, skiprows = skip - intSkip - 1, nrows = 1, delimiter="?")
    df4["mTime"] = pd.to_datetime(df4["mTime"])
    
    df5 = pd.read_csv(html, names = colNames5, skiprows = skip - intSkip, nrows = 1, delimiter="=")
    del df5["junk"]
    df5["iteration"][0] = df5.iloc[0]["iteration"].split("<")[0]

    df = pd.concat([df1,df2,df3,df4, df5], axis=1)
    return df


"""
