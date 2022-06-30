#!/usr/bin/env python3

import mysql.connector
import string
import random

cnx = mysql.connector.connect(user='root',
                              password='mypass',
                              host='127.0.0.1',
                              database='employees'
                             )

query = "SELECT * FROM employees limit 10"
cursor = cnx.cursor()
cursor.execute(query, ())

y = list(cursor)

## Creaate a table to pad out some data

employee_extra_data_SQL = """
CREATE TABLE employee_extra (
    emp_no      INT      NOT NULL,
    extra_id    INT NOT NULL AUTO_INCREMENT,
    extra_val   LONGTEXT NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
    PRIMARY KEY (extra_id)
);
"""

def getTables(cursor):
    cursor.execute("show tables;", ())
    t = list(cursor)
    tl = [x[0] for x in t]
    return(tl)


def printTablesList(tlist):
    print("TABLES:")
    for i,t in enumerate(tlist):
        print(f"{i}: {t}")

letters = string.ascii_letters
def makeRandomString(slen):
    return(''.join(random.choice(letters) for i in range(slen)))

def getEmployeeIds(cursor):
    cursor.execute("SELECT DISTINCT emp_no from employees")
    t = list(cursor)
    return([x[0] for x in t])



tables_pre = getTables(cursor)

if 'employee_extra' not in tables_pre:
    print("Missing employee_extra table. Inserting.")
    cursor.execute(employee_extra_data_SQL, ())
    r = list(cursor)


tables_post = getTables(cursor)
empIds = getEmployeeIds(cursor)

def mkRandExtraData(N, 
                    empIds,
                    cnx,
                    cursor,
                    data_size = 10000                    
                    ):
    
    for i in range(1, N+1):
        emp_id = random.choice(empIds)
        istr = ("INSERT INTO employee_extra " 
                "(emp_no, extra_val) "
                "VALUES (%s, %s)")
        ival = (emp_id, makeRandomString(data_size))
        cursor.execute(istr, ival)
        if (i) %100 == 0:
            print(f"Inserted {i}/{N}")
        
    print(f"DONE: Inserted {i}/{N}")
    cnx.commit()


mkRandExtraData(1337, empIds, cnx, cursor)

mkRandExtraData(31337, empIds, cnx, cursor)

cnx.close()