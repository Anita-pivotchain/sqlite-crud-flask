
from crypt import methods
from csv import QUOTE_NONE, QUOTE_NONNUMERIC
import re
from unittest import result
from flask import Flask,request,jsonify
from sqlalchemy import Table,Column
import json
from sqlalchemy.sql.sqltypes import NUMERIC,VARCHAR,Integer
from sqlalchemy import create_engine,MetaData,or_
from pydantic import BaseModel


app=Flask(__name__)



engine = create_engine("sqlite:///Studinfo1.db",connect_args={'check_same_thread': False})
''' 
The create_engine() method of sqlalchemy library takes in the connection and returns a sqlalchemy 
engine that references both a Dialect and a Pool, which together interpret the DBAPIs module functions
as well as the behavior of the database.
In this example, a sqlalchemy engine connection has been established with the sqlite database.
'''

meta = MetaData(bind=engine)

#create table 

'''
Column object represents a column in a database table. Constructor takes name, 
type and other parameters such as primary_key, autoincrement and other constraints.
'''
Studinfo = Table(
    'Studinfo', meta,
    Column('id', Integer, primary_key=True,autoincrement=True),
    Column('name', VARCHAR),
    Column('gender',VARCHAR),
    Column('age', Integer),
    Column('std',Integer)

)
  
meta.create_all(engine)  
'''The create_all() function uses the engine object to create all the defined table objects and stores the information in metadata.'''


#--------------------------Insert----------------------------------------------
  
'''The SQL INSERT INTO statement of SQL is used to insert a new row in a table. There are two ways of using the INSERT INTO
 statement for inserting rows:
 Only values: The first method is to specify only the value of data to be inserted without the column names.
 Column names and values both: In the second method we will specify both the columns which we want to fill and their corresponding values 
 '''  
@app.route('/insert',methods=['POST'])
def write_data():
    info = request.get_json()
    engine.execute(Studinfo.insert().values(info))
    # results = [list(row) for row in result]
    # result_dict = {'results': results}
    return jsonify("---Data inser successfully---")


#---------------------------Display---------------------------------------------

@app.route('/read',methods=['GET'])
def read_info():

     '''SELECT is used to retrieve data from an SQLite table and this returns the data contained in the table.'''

     sql = text('SELECT * from Studinfo')
     result= engine.execute(sql)
     
     return jsonify({"result":[dict(row) for row in result]})

@app.route('/readby/<id>',methods=['GET'])
def read_info_by_id(id):
    result=engine.execute(Studinfo.select().where(Studinfo.c.id==id)).fetchall() 
    '''
    Now use the Select statement to retrieve data from the table and fetch all records.
    To fetch all records we will use fetchall() method.
    
    '''
    return jsonify({"result":[dict(row) for row in result]})   



#-----------------------------------Read by any------------------------------------

@app.route('/readbyany',methods=['GET'])
def read_info1():

    info = request.json
    def send_format(a):
        try:
            b = int(a)
            return a
        except:
            return "'"+a+"'"

    '''The WHERE clause of SELECT query can be for the condition .'''        
    t = engine.execute("select * from Studinfo where  %s=%s " %(list(info["set"].keys())[0], send_format(list(info["set"].values())[0]))) .fetchall()
    return jsonify({"result":[dict(row) for row in t]})   



#------------------------------------------Update--------------------------------

@app.route('/update',methods=['PUT'])
def update():

    info = request.json
    def send_format(a):
        try:
            b = int(a)
            return a
        except:
            return "'"+a+"'"

    '''The SET conditions are determined from those parameters passed to the statement during the execution
     and/or compilation of the statement.The where clause is an Optional expression describing the WHERE condition of the UPDATE statement.
    '''        

    t = engine.execute("UPDATE Studinfo SET %s=%s WHERE %s==%s " %(list(info["set"].keys())[0], send_format(list(info["set"].values())[0]), list(info["cond"].keys())[0],send_format(list(info["cond"].values())[0])))
    return jsonify("data update successfully")   
    


#--------------------------------------delete-----------------------------------------------------

@app.route('/delete/<id>',methods=['DELETE'])
def delete(id):
    result=engine.execute(Studinfo.delete().where(Studinfo.c.id==id))
    '''
    In SQLite database we use the delete query for delete the data from a table:
    DELETE FROM table_name [WHERE Clause]
    '''

    return jsonify({"result":[dict(row) for row in result]})   


@app.route('/delete',methods=['DELETE'])
def deleteany():
    info = request.json
    def send_format(a):
        try:
            b = int(a)
            return a
        except:
            return "'"+a+"'"
    engine.execute("delete from Studinfo where  %s=%s " %(list(info["set"].keys())[0], send_format(list(info["set"].values())[0])))
    return jsonify("--- Data Deleted--- ")   


if __name__ == '__main__':
  app.run(debug=True,port=5007)    