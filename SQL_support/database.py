import MySQLdb
# import Data_structure.Entity as En

class db_interpreter:
    def __init__(self,impl,host="localhost",user="root",passwd="metro22"):
       self.db1 = MySQLdb.connect(host,user,passwd)
       self.implementation = impl
       self.cursor = self.db1.cursor()
       self.doneRelations = []
       self.queries = []

    def create_database(self,dbName="test_image"):
        sql = 'CREATE DATABASE IF NOT EXISTS'+dbName
        self.queries.append(sql+";")
        if self.implementation :
            self.cursor.execute(sql)

    def create_table(self, entity):
        sql = "CREATE TABLE "+entity.name+" ("

        for attrib in entity.attr_list:
            if attrib.isComposite == True:
                for child_attrib in attrib.attrib_childs:
                    sql += " "+child_attrib.name + " CHAR(40) ,"
            else:
                if attrib.type == "prime" or attrib.type == "primary":
                    sql += " "+attrib.name + " INT(20) PRIMARY KEY AUTO_INCREMENT,"
                else:
                    sql += " "+attrib.name + " CHAR(40) ,"

        if sql[-1] !=")": 
            if sql[-1]==",":
                sql2 = sql[:-1]+")"
                self.queries.append(sql2+";")
            else:
                sql += ")"
                self.queries.append(sql+";")
        else:
            self.queries.append(sql+";")

        if self.implementation :
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
        res = self.__addForignKey(parameter_list)
        sql = "ALTER TABLE "+parameter_list[2].name +\
              " ADD CONSTRAINT "+parameter_list[2].name+"_unique"+" UNIQUE ("+res+")"
        self.queries.append(sql+";")
        if self.implementation :
            self.cursor.execute(sql)

    def __MakeOneToMany(self, parameter_list):
        if parameter_list[1].p_ratio1 == "one":
            self.__addForignKey(parameter_list)
        else:
            parameter_list[0],parameter_list[2] = parameter_list[2],parameter_list[0]
            self.__addForignKey(parameter_list)

    def __MakeManyToMany(self, parameter_list):
        table_name = parameter_list[1].name
        PK_tableA = parameter_list[0].getprim_attrib().name
        PK_tableB = parameter_list[2].getprim_attrib().name

        sql = "CREATE TABLE " + table_name +"("+\
               PK_tableA + "SMALLINT UNSIGNED NOT NULL DEFAULT 0 ,"+\
               PK_tableB + "SMALLINT UNSIGNED NOT NULL DEFAULT 0 ,"
              

        for attrib in parameter_list[1].attrib_list:
            sql += " "+attrib.name + " CHAR(40) ,"

        sql += "CONSTRAINT pk_"+table_name + "PRIMARY KEY ("+PK_tableA+","+PK_tableB+"))"

        if sql[-1] !=")": sql += ")"
        self.queries.append(sql+";")
        if self.implementation :
            self.cursor.execute(sql)      

    def __addForignKey(self,parameter_list):        #  adds a fk in tableB that refrences the pk in tableA
        fk_name = parameter_list[0].getPrim_attrib().name
        sql = "ALTER TABLE "+parameter_list[2].name +\
              " ADD "+ fk_name+"_fk" + " SMALLINT UNSIGNED NOT NULL DEFAULT 0"

        sql2 = "ALTER TABLE "+parameter_list[2].name +" ADD CONSTRAINT fk_"+fk_name+\
               " FOREIGN KEY (" + fk_name+"_fk" + ") REFERENCES "+parameter_list[0].name+"("+fk_name+")"

        if self.implementation :
            self.cursor.execute(sql)
            self.cursor.execute(sql2)

        self.queries.append(sql+";")
        self.queries.append(sql2+";")
        return fk_name

    def __del__(self):
        self.db1.commit()
        self.db1.close()
        print("connection with db is closed")