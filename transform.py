__author__ = 'Daniel'

import pandas as pd
import os
import xlrd

#dfinputdata = DataFrame()

df1 = pd.DataFrame()

for subdir, dirs, files in os.walk('.\\Input'):
    for file in files:
        df2 = pd.DataFrame()

        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        print(filepath)
        #df1 = pd.read_excel(filepath)

        df2 = pd.read_csv(filepath, "Sheet 1")
        #df2 = df2[df2[1] != NaN]
        for row in df2.iterrows():
            #print("Row")
            print("Row:", row)
            print(row)
        print(df2)

        #df2 = xl.parse()

        #print("Reading file", filepath)
        #with filepath as csv:
            #a = 2
            #print(xls)
            #, 'Sheet1', 1, None, None, 4, None, None, True, False, None)
        #if filepath.endswith(".asm"):
        #    print (filepath)


print(df1)

#conn = sqlite3.connect('example.db')