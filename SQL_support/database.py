import MySQLdb
from PyQt5.QtWidgets import QMessageBox
# import Data_structure.Entity as En

class db_interpreter:
    def __init__(self,impl,host="localhost",user="root",passwd="metro22"):
       self.implementation = impl
       if impl:
           try:
            self.db1 = MySQLdb.connect(host,user,passwd)
           except:
            err =  QMessageBox(text="error conecting to mysql server")
            err.show()
            self.implementation = False
           else:
            self.cursor = self.db1.cursor()

       self.doneRelations = []
       self.queries = []

    def create_database(self,dbName="test_image"):
        sql = """CREATE DATABASE IF NOT EXISTS """+dbName
        self.queries.append(sql+";")
        self.queries.append("USE "+dbName+" ;")
        if self.implementation :
            self.cursor.execute(sql)
            self.cursor.execute("USE "+dbName)

    def create_table(self, entity):
        sql = """CREATE TABLE """+entity.name+""" ("""

        for attrib in entity.attr_list:
            if attrib.type == "prime" or attrib.type == "primary" or attrib.type == "Prime":
                if attrib.isComposite == True:
                    for child_attrib in attrib.attrib_childs:
                        sql += """ """ + child_attrib.name + """ INT NOT NULL DEFAULT 0 ,"""
                    sql += "CONSTRAINT pk_" + entity.name + " PRIMARY KEY ("
                    for child_attrib in attrib.attrib_childs:
                        sql += child_attrib.name + """ ,"""
                    sql=sql[:len(sql)-1]
                    sql+=")"+")"
                else:
                    sql += """ """ + attrib.name + """ INT(20) PRIMARY KEY AUTO_INCREMENT,"""


            elif attrib.isComposite == True:
                for child_attrib in attrib.attrib_childs:
                    sql += """ """+child_attrib.name + """ CHAR(40) ,"""
            else:
                if attrib.type == "prime" or attrib.type == "primary"or attrib.type == "Prime":
                    sql += """ """+attrib.name + """ INT(20) PRIMARY KEY AUTO_INCREMENT,"""
                else:
                    sql += """ """+attrib.name + """ CHAR(40) ,"""

        if sql[-1] !=")":
            if sql[-1]==",":
                sql2 = sql[:-1]+""")"""
                self.queries.append(sql2+";")
                sql = sql2
            else:
                sql += ")"
                self.queries.append(sql+";")
        else:
            self.queries.append(sql+";")

        if self.implementation :
            # self.create_database()
            self.cursor.execute(sql)


# [TODO] change this redirection algorithm with polymorphism of relation in refactoring phase

    def create_relation(self,params):   #params are [TableA,relation,TableB]
        if self.__isDone(params[1]):
            return

        if self.__isOneToMany(params[1]):
            self.__MakeOneToMany(params)

        elif self.__isOneToOne(params[1]):
            self.__MakeOneToOne(params)

        elif self.__isManyToMany(params[1]):
            self.__MakeManyToMany(params)

        else:
            raise ValueError
        self.doneRelations.append(params[1].id)

    def __isDone(self, relation):
        try:
            self.doneRelations.index(relation.id)
            return 1

        except ValueError as RelationNotFound:
            print("relation with ID : {}    Name: {} Not found".format(relation.id,relation.name))
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
    #---------relation handels-----------
    def __MakeOneToOne(self, parameter_list):
        self.__addForignKey(parameter_list)
        # sql = "ALTER TABLE "+parameter_list[2].name +\
        #       " ADD CONSTRAINT "+parameter_list[2].name+"_unique"+" UNIQUE ("+res+"_fk"+")"
        # self.queries.append(sql + ";")
        if (len(parameter_list[1].attrib_list) != 0):
            sql2="ALTER TABLE "+parameter_list[2].name



            for attrib in  parameter_list[1].attrib_list:
                sql2+=" ADD"+" "+attrib.name+" char(40)"+","
            sql2=sql2[:len(sql2)-1]+""
            self.queries.append(sql2+";")
            if self.implementation:
                self.cursor.execute(sql2)

        # if self.implementation :
        #     self.cursor.execute(sql)


    def __MakeOneToMany(self, parameter_list):
        if parameter_list[1].p_ratio1 == "many":
            self.__addForignKey(parameter_list)
            if (len(parameter_list[1].attrib_list) != 0):

                sql2 = "ALTER TABLE " + parameter_list[2].name

        else:
            parameter_list[0],parameter_list[2] = parameter_list[2],parameter_list[0]
            self.__addForignKey(parameter_list)
            if (len(parameter_list[1].attrib_list) != 0):
                sql2 = "ALTER TABLE " + parameter_list[2].name


        if (len(parameter_list[1].attrib_list) != 0):
            for attrib in parameter_list[1].attrib_list:
                sql2 += " ADD"+" " + attrib.name + " char(40)" + ","
            sql2 = sql2[:len(sql2) - 1] + ""
            self.queries.append(sql2 + ";")

            if self.implementation:
                self.cursor.execute(sql2)

    def __MakeManyToMany(self, parameter_list):
        table_name = parameter_list[1].name
        PK_tableA=""
        A_type=""
        PK_tableB=""
        B_type=""
        if ( not parameter_list[0].getPrim_attrib().isComposite):
            PK_tableA = parameter_list[0].getPrim_attrib().name
            A_type = PK_tableA+" INT NOT NULL DEFAULT 0 ,"
        else:
            for attrib in parameter_list[0].getPrim_attrib().attrib_childs:
                PK_tableA+=attrib.name+","
                A_type+=attrib.name+" INT NOT NULL DEFAULT 0 ,"
            PK_tableA = PK_tableA[:-1]
        if (not parameter_list[2].getPrim_attrib().isComposite):
            PK_tableB = parameter_list[2].getPrim_attrib().name
            B_type =PK_tableB+" INT NOT NULL DEFAULT 0 ,"
        else:
            for attrib in parameter_list[2].getPrim_attrib().attrib_childs:
                PK_tableB+=attrib.name+","
                B_type+=attrib.name+" INT NOT NULL DEFAULT 0 ,"
            PK_tableB = PK_tableB[:-1]

        sql = "CREATE TABLE " + table_name +"("+A_type  +B_type
        sql2 = "ALTER TABLE "+table_name +" ADD CONSTRAINT fk_"+parameter_list[0].name +\
               " FOREIGN KEY (" + PK_tableA + ") REFERENCES "+parameter_list[0].name+"("+PK_tableA+")"
        sql3 ="ALTER TABLE "+table_name +" ADD CONSTRAINT fk_"+parameter_list[2].name +\
               " FOREIGN KEY (" + PK_tableB + ") REFERENCES "+parameter_list[2].name+"("+PK_tableB+")"

        for attrib in parameter_list[1].attrib_list:
            sql += " "+attrib.name + " CHAR(40) ,"

        sql += "CONSTRAINT pk_"+table_name + " PRIMARY KEY ("+PK_tableA+","+PK_tableB+"))"

        if sql[-1] !=")": sql += ")"
        self.queries.append(sql+";")
        self.queries.append(sql2+";")
        self.queries.append(sql3+";")
        if self.implementation :
            self.cursor.execute(sql)
            self.cursor.execute(sql2)
            self.cursor.execute(sql3)


    def __addForignKey(self,parameter_list):        #  adds a fk in tableB that refrences the pk in tableA
        if(parameter_list[0].getPrim_attrib().isComposite == False):
            fk_name = parameter_list[0].getPrim_attrib().name
            sql = "ALTER TABLE "+parameter_list[2].name +\
                  " ADD "+ fk_name+"_fk" + " INT NOT NULL DEFAULT 0"

            sql2 = "ALTER TABLE "+parameter_list[2].name +" ADD CONSTRAINT fk_"+fk_name+\
                   " FOREIGN KEY (" + fk_name+"_fk" + ") REFERENCES "+parameter_list[0].name+"("+fk_name+")"

            if self.implementation :
                self.cursor.execute(sql)
                self.cursor.execute(sql2)

            self.queries.append(sql+";")
            self.queries.append(sql2+";")
        else:
            sql="ALTER TABLE "+parameter_list[2].name

            sql2="ALTER TABLE "+parameter_list[2].name +" ADD CONSTRAINT fk_"+parameter_list[0].name

            sql2_1=" FOREIGN KEY ("
            sql2_2=" REFERENCES "+parameter_list[0].name+"("
            for attrib in  parameter_list[0].getPrim_attrib().attrib_childs :
                sql+=" ADD "+"fk_"+attrib.name+ " INT NOT NULL DEFAULT 0"+","
                sql2_1+="fk_"+attrib.name + ","
                sql2_2+=attrib.name + ","
            sql=sql[:-1]
            sql2_1=sql2_1[:-1]
            sql2_2=sql2_2[:-1]
            sql2_1+=" )"
            sql2_2+=" )"
            sql2+=sql2_1+sql2_2
            if self.implementation :
                self.cursor.execute(sql)
                self.cursor.execute(sql2)

            self.queries.append(sql+";")
            self.queries.append(sql2+";")

    def __del__(self):
        if self.implementation:
            self.db1.commit()
            self.db1.close()
            print("connection with db is closed")