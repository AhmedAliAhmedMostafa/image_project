#output of the imag-processing phase and gui phsase would be a list of class entity and a list of class relation 



class entity:
    def __init__(self,i,n):
        self.id =i #unique number for each entity
        self.name =n #name image processing part give to each entity a name like "entity-1" then Gui Module ask user to change name to whatever he/she likes
        self.attr_list = [] #a list that contain all the entity atttribute each member of the list is instance of class attribute
    def add_attr(self,attr):
        self.attr_list.append(attr)


class attribute :
    def __init__(self,name,type):
        self.name = name # name of attribute image processing part give to each attribute  a name like "attribute-1-1" then Gui Module ask user to change name to whatever he/she likes
        self.type = type # type would be a primary key or non prime

class relation :
    def __init__(self,name,id1,id2,p_ratio1,p_ratio2,p_type1,p_type2):
        self.name = name
        self.id1 = id1 #id of the first entity in the relation
        self.id2 = id2 #id of the second entity in the relation
        self.p_type1 = p_type1 #type  of participation of the first entity could be partial or full
        self.p_type2 = p_type2 #type of participation of the second entity could be partial or full
        self.p_ratio1  = p_ratio2 #ratio of participation of first entity could be one or many
        self.p_ratio2  = p_ratio2 #ratio of participation of second  entity could be one or many





