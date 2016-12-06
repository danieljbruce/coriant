__author__ = 'Daniel'

from pandas import *
import pandasql
import sqlite3
import datetime

# datetime.datetime.now().strftime("%I:%M%:%S%p on %B %d, %Y")

def PrepareData(pDataBaseName = 'coriant.db'):
    # Cleans and formats the dataframe ready for the most natural way to work with it
    # Returns:

    conn = sqlite3.connect(pDataBaseName)
    sql = 'SELECT * FROM session'
    runningdate = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = 'Coriant_Invoice_' + runningdate

    pysql = lambda q: pandasql.sqldf(q, globals())

    df = pandas.read_sql(sql, conn, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)

    #df2 = pandas.DataFrame(columns=['Tutors', 'Date', 'Time', 'Student'])

    df_fulldetail_list = []

    for index, row in df.iterrows():
        students = row['Students']
        if students is not None:
            students_list = students.split(',')
            for s in students_list:
                s = s.strip()
                print(s)
                #dftemp = pandas.DataFrame([row['Tutors'], row['Date'], row['Time'], s], columns=['Tutors', 'Date', 'Time', 'Student'])
                df_fulldetail_list.append({'Tutors' : row['Tutors'], 'Date' : row['Date'], 'Month' : row['Date'][:-3], 'Time' : row['Time'], 'Student' : s, 'Students' : students})
                # print(row['Students'], index)

    df_fulldetail = pandas.DataFrame(df_fulldetail_list)

    df_dates_only = df_fulldetail['Date']
    df_tutors_only = df_fulldetail['Tutors']
    df_students_only = df_fulldetail['Student']
    df_month_only = df_fulldetail['Month']

    list_date = df_dates_only.drop_duplicates().values.tolist()
    list_students = df_students_only.drop_duplicates().values.tolist()
    list_tutors = df_tutors_only.drop_duplicates().values.tolist()
    list_months = df_month_only.drop_duplicates().values.tolist()
    #df_months = pandas.DataFrame([i[:-3] for i in list_date])
    #list_months = df_months.drop_duplicates().values.tolist()
    # Print sheet with overall invoice, tutor drilldown and student drilldown.

    #MONTH(Date) as 'Month',
    # , 'Month'
    for i in list_months:
        # Now write overall invoice, tutor based invoice and student invoice
        # Overall
        df_month = df_fulldetail[df_fulldetail.Month == i]
        writer = ExcelWriter('./Output/Invoice_' + runningdate + '_month_' + i +'.xlsx')
        df_month.to_excel(writer,"Overall")
        #print(i)
        # Tutor
        for j in list_tutors:
            df_tutor = df_month[df_month.Tutors == j]
            df_tutor.to_excel(writer,j)
            for k in list_students:
                # Student
                df_students = df_tutor[df_tutor.Student == k]
                df_students.to_excel(writer,j + "_" + k)
        writer.save()

    # str1 = "SELECT Tutors, Date, Time, Students, COUNT(*) AS 'Total' FROM df_fulldetail GROUP BY Tutors, Date, Time, Students;"
    # df_student_detail = pysql(str1)

    print(df_fulldetail)
    print("Dates only:")
    print(list_date)
    print("Students only:")
    print(list_students)
    print("Tutors:")
    print(list_tutors)
    print("Months:")
    print(list_months)
    print(runningdate)


# >>> writer = ExcelWriter('output.xlsx')
# >>> df1.to_excel(writer,'Sheet1')
# >>> df2.to_excel(writer,'Sheet2')
# >>> writer.save()