#!/usr/bin/env python3

import mysql.connector
import string
import random
from itertools import islice
import argparse



## SQL to create extra data table
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

def group_elements(lst, chunk_size):
    lst = iter(lst)
    return iter(lambda: tuple(islice(lst, chunk_size)), ())

def mkRandExtraData(N, 
                    empIds,
                    cnx,
                    cursor,
                    data_size = 10000                    
                    ):
    
    emp_id_samples = random.choices(empIds, k=N)
    emp_id_groups  = group_elements(emp_id_samples, 1000)
    istr = "INSERT INTO employee_extra (emp_no, extra_val) VALUES (%s, %s)"

    # Iteate over the chunks
    ins_count = 0
    for i_g, xs in enumerate(emp_id_groups):
        emp_id_sublist = list(xs)
        rand_data = [makeRandomString(data_size) for i in emp_id_sublist]
        sub_data = list(zip(emp_id_sublist, rand_data))
        cursor.executemany(istr, sub_data)
        cnx.commit()
        ins_count = ins_count + len(sub_data)
        print(f"Group {i_g + 1}. Inserted {ins_count}/{N}")

    
    print(f"DONE: Inserted {ins_count}/{N}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", help='Number of sample entries', type=int, required=True)
    args = parser.parse_args()
    print(args)

    cnx = mysql.connector.connect(user='root',
                                password='mypass',
                                host='127.0.0.1',
                                database='employees'
                                )


    # Make the new table if necessary
    cursor = cnx.cursor()
    tables_pre = getTables(cursor)
    if 'employee_extra' not in tables_pre:
        print("Missing employee_extra table. Inserting.")
        cursor.execute(employee_extra_data_SQL, ())
        r = list(cursor)
    else:
        print("employee_extra table present.")
        
    tables_post = getTables(cursor)

    empIds = getEmployeeIds(cursor)

    num_samples = args.num
    print(f"Called with {num_samples}")
    mkRandExtraData(num_samples, empIds, cnx, cursor)
    cnx.close()


