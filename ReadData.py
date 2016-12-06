__author__ = 'Daniel'

import sqlite3, csv
import pandas
import os

def ReadData(pDataBaseName = 'coriant.db'):
    conn = sqlite3.connect(pDataBaseName)

    # Run SQL query to delete existing data.
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS session(Tutors TEXT, Date NUMERIC, Time NUMERIC, Students TEXT)''')
    c.execute('''DELETE FROM session''')

    source = os.getcwd() + "\Input\\"
    destination = os.getcwd() + "\Input Processed\\"
    print "Reading directory", source
    for i in os.listdir(source):
        print "Observing file", i
        if i.endswith(".csv"):
            print "Processing file", source + i
            df = pandas.read_csv(source + i)
            df.columns = ['Tutors', 'Date', 'Time', 'Students']
            df.to_sql('session', conn, if_exists='append', index=False)
            # source = os.getcwd() + "\Input\\"
            # os.rename(source + i, destination + i)
            print "Finished processing file", source + i
            continue
        else:
            continue
    conn.close()

def ProcessData(pDataBaseName = 'coriant.db'):
    ReadData(pDataBaseName)
    conn = sqlite3.connect(pDataBaseName)
    c = conn.cursor()
    c.execute('''DELETE FROM session WHERE Tutors IS NULL''')
    conn.close()

ProcessData()
os.system("pause")