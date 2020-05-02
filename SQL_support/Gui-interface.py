from database import db_interpreter

db = db_interpreter()
def create_SQL(gui_list_of_entities):
    '''
    @description: takes list of entites as in Entity.py and creates connection with mysql db making
                  queires deived from entity objects [intended to be triggered by a button from GUI]

    @input      : list of entites
    @output     : None or Error(if supported error reporting)
    '''
    pass