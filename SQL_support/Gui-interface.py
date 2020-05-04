# from SQL_support.database import db_interpreter
from database import db_interpreter

def path_resolve():
    ExecutionPath = importPath = os.getcwd()
    #os.chdir("..")
    sys.path.insert(1, importPath+"/Data_structure/")
    os.chdir(ExecutionPath)   

import sys,os
path_resolve()

import Entity as En
# import Data_structure.Entity as En
__all__=["Entity"]

def create_SQL(gui_list_of_entities,implementation=False):
    '''
    @description: takes list of entites as in Entity.py and creates connection with mysql db making
                  queires derived from entity objects [intended to be triggered by a button from GUI]

    @input      : list of entites
    @output     : None or Error(if supported error reporting)
    '''
    db = db_interpreter(impl=implementation)
    for entity in gui_list_of_entities:
        db.create_table(entity)

    for entity in gui_list_of_entities:
        for rel in entity.relations:
            traget_entity = getEntityByID(gui_list_of_entities,rel.getTargetEntity(entity))
            db.create_relation([entity,rel,traget_entity])

    
    exportQuery(db.queries)
    
def getEntityByID(entity_list,id):
    for entity in entity_list:
        if entity.id == id :
            return entity

def exportQuery(queries,option="txt"):
    if option == "txt":
        text_file = open("Queries.txt", "w")
        for query in queries:
            text_file.write(query+"\n")
        text_file.close()
    else:
        raise NotImplementedError("ONLY text format is supported")


def main():# [FOR TESTING ONLY]
    #----------tables/relation creation--------------
    EmployeeEntity =  En.entity("employee")
    departmentEntity = En.entity("Department")
    emp_dep_Relation = En.relation("work-for",EmployeeEntity.getID(),departmentEntity.getID(),"one","many","full","full")
    EmployeeEntity.add_relation(emp_dep_Relation)
    departmentEntity.add_relation(emp_dep_Relation)

    # ----------tables attribute----------------------
    Ename = En.attribute("Ename","non-prime")
    SSID = En.attribute("SSID","prime")

    EmployeeEntity.add_attr(Ename)
    EmployeeEntity.add_attr(SSID)

    dName = En.attribute("Dname","prime")
    dlocation = En.attribute("location","non-prime")
    manger = En.attribute("manager","non-prime")

    departmentEntity.add_attr(dName)
    departmentEntity.add_attr(dlocation)
    departmentEntity.add_attr(manger)

    entities=[EmployeeEntity,departmentEntity]

    create_SQL(entities)

    # db = MySQLdb.connect( "localhost" ,"root" , "metro22" ,"test_image")
    # # prepare a cursor object using cursor() method
    # cursor = db.cursor()

    # # execute SQL query using execute() method.
    # cursor.execute("SELECT VERSION()")

    # # Fetch a single row using fetchone() method.
    # data = cursor.fetchone()
    # print ("Database version : %s " % data)

    # # disconnect from server
    # db.close()
if __name__ == "__main__":
    main()