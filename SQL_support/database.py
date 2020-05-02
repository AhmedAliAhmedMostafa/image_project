import sys,os
ExecutionPath = importPath = os.getcwd()
#os.chdir("..")
sys.path.insert(1, importPath+"/Data_structure/")
os.chdir(ExecutionPath)

import MySQLdb
import Entity as En
__all__=["Entity"]

class db_interpreter:
    def __init__(self,host="localhost",user="root",passwd="metro22"):
       self.db1 = MySQLdb.connect(host,user,passwd)
       self.cursor = db1.cursor()
       self.doneRelations = []

    def create_database(self,dbName="test_image"):
        sql = 'CREATE DATABASE IF NOT EXISTS'+dbName
        cursor.execute(sql)

    def create_table(self, entity):
        sql = "CREATE TABLE "+entity.name
        cursor.execute(sql)

    def create_relation(self,relation):
        if self.__isDone(relation):
            return
        if self.__isOneToMany(relation):
            pass
        elif self.__isOneToOne(relation):
            pass
        elif self.__isManyToMany(relation):
            pass
        else:
            raise ValueError

    def __isDone(self, relation):
        try:
            self.doneRelations.index(relation.id)
            return 1 

        except ValueError as RelationNotFound:
            return 0

    #---------relation predicates-----------
    def __isOneToMany(self,relation):
        if (relation.p_ratio1=="one" and relation.p_ratio2=="many") or (relation.p_ratio2=="one" and relation.p_ratio1=="many"):
            return 1
        return 0

    def __isManyToMany(self,relation):
        if relation.p_ratio1=="many" and relation.p_ratio2=="many":
            return 1
        return 0

    def __isOneToOne(self,relation):
        if relation.p_ratio1=="one" and relation.p_ratio2=="one":
            return 1
        return

    def __del__(self):
        self.db1.commit()
        self.db1.close()
        print("connection with db is closed")



def main():
    #----------tables/relation creation--------------
    EmployeeEntity =  En.entity("employee")
    departmentEntity = En.entity("Department")
    emp_dep_Relation = En.relation("work-for",EmployeeEntity.getID(),departmentEntity.getID(),"full","full","one","many")
    EmployeeEntity.add_relation(emp_dep_Relation)
    departmentEntity.add_relation(emp_dep_Relation)

    # ----------tables attribute----------------------
    Ename = En.attribute("Ename","non-prime")
    SSID = En.attribute("SSID","prime")

    EmployeeEntity.add_attr(Ename)
    EmployeeEntity.add_attr(SSID)

    dName = En.attribute("Dname","non-prime")
    dlocation = En.attribute("location","non-prime")
    manger = En.attribute("manager","non-prime")

    departmentEntity.add_attr(dName)
    departmentEntity.add_attr(dlocation)
    departmentEntity.add_attr(manger)

    entities=[EmployeeEntity,departmentEntity]

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