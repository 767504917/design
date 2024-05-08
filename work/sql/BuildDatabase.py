# -*- coding = utf-8 -*-
# @Time :2024/4/27 21:29
import sqlite3
from datetime import date
def buildDatabase():
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS user(
    user_id     INT     not null,
    username    TEXT    not null,
    password    TEXT    not null,
    PRIMARY KEY(user_id)
    );
    ''')
    cur.execute('''
            CREATE TABLE IF NOT EXISTS advice_table(
            patient_id     INT     not null,
            patient_name    TEXT    not null,
            patient_age    TEXT    not null,
            advice    TEXT    not null,
            image_path      TEXT        not null,
            advice_time      TEXT     not null,
            PRIMARY KEY(patient_id)
            );
            ''')
    connect.commit()#提交
    connect.close()
def loginCheck(name,pwd):
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    cur.execute('''
    SELECT * from user where username=?
    ''',(name,))
    connect.commit()
    result = cur.fetchone()
    connect.close()
    if result[2] == pwd:
        return True
    return False
def give_advice(patient_name,patient_age,advice,image_path):
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    cur.execute('''
    SELECT count(*) from advice_table;
    ''')
    today = date.today()
    rows = int(cur.fetchone()[0])#advice_id
    advice_info = [rows + 1,patient_name,patient_age,advice,image_path,today.strftime("%Y-%m-%d")]
    cur.execute('''INSERT INTO advice_table(patient_id,patient_name,patient_age,advice,image_path,advice_time)
        VALUES (?,?,?,?,?,?);
        ''',advice_info)
    connect.commit()  # 提交

    connect.close()
def getTable():
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    cur.execute('''
        SELECT * from advice_table ORDER BY patient_id DESC;
        ''')

    allItems = cur.fetchall()

    connect.commit()  # 提交
    connect.close()
    return allItems
def advice_by_id(id):
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    cur.execute('''
       SELECT * from advice_table where patient_id=?
       ''', (id,))
    item = cur.fetchone()
    advice = item[3]
    img_path = item[4]
    connect.commit()  # 提交
    connect.close()
    return advice,img_path