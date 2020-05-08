from PyQt5.QtWidgets import QApplication,QGraphicsView,QGraphicsScene,QLineEdit,QMessageBox,QLabel,QGraphicsLineItem,QGraphicsEllipseItem,QMainWindow,QFileDialog,QPushButton,QGridLayout,QDialog
from PyQt5.QtCore import Qt,QRectF,QPointF,QLineF,QSize,QRect
from PyQt5.QtGui import QPainter,QBrush,QPen,QColor,QPolygonF,QIcon,QPixmap
from Data_structure import Entity as En
from image_processing import Image as image
import cv2
import  sys
from functools import partial
from SQL_support import Gui_interface



class ContainerItem:
    def __init__(self,entity,pos,scene):
        self.entity_width = 180
        self.entity_height = 80
        self.entity_pen = QPen(Qt.black,5,Qt.SolidLine)
        self.entity_brush =QBrush(Qt.green,Qt.SolidPattern)

        self.attribute_width = 90
        self.attribute_height = 50
        self.attribute_pen  = QPen(Qt.black,3,Qt.SolidLine)
        self.attribute_brush  = QBrush(Qt.blue,Qt.Dense6Pattern)

        self.at_connection_pen  = QPen(Qt.black,3,Qt.SolidLine)
        self.entity = entity
        self.no_atr =len(self.entity.attr_list)
        self.inter_atr_margin = 15
        self.min_height =-50
        self.container_width  = self.entity_width +self.attribute_width
        self.container_height = -1*self.min_height*self.no_atr + self.attribute_height
        self.en_shape = scene.addRect(QRectF(0,0,self.entity_width,self.entity_height),self.entity_pen,self.entity_brush)

        self.txt_style = ''' QWidget{border:3px dashed black;padding-bottom:5px;} '''
        self.txt_en_geometry = QRectF(0.0, 0.0, self.entity_width / 2, self.entity_height / 2)
        self.txt_atr_geometry = QRectF(0.0, 0.0, self.attribute_width / 2, self.attribute_height / 2)
        self.txt_atr_child_geometry = QRectF(0.0, 0.0, self.attribute_width / 2, self.attribute_height /2)
        self.txt_atr_pos = QPointF(self.attribute_width/4,self.attribute_height/4)
        self.txt_en_pos =  QPointF(self.entity_width / 4, self.entity_height / 4)

        self.en_txt = scene.addWidget(QLineEdit())
        self.en_txt.setParentItem(self.en_shape)
        self.en_txt.setGeometry(self.txt_en_geometry)
        self.en_txt.widget().setStyleSheet(self.txt_style)
        self.en_txt.widget().setText(self.entity.name)
        self.en_txt.setPos(self.txt_en_pos)

        self.en_txt.widget().editingFinished.connect( lambda :ContainerItem.trial(self,-1,self.en_txt.widget(),0))

        self.scene = scene
        self.en_shape.setPos(pos)
        self.con_list = []
        self.atr_shape_list = []
        self.atr_txt_list = []
        self.rel_orgn = QPointF(0,self.entity_height)
        self.orgn_step =15
        self.id=0


        if(self.no_atr>1):
            self.atr_step = self.entity_width / (self.no_atr - 1)

            if(2*self.atr_step <self.attribute_width):

                self.attribute_width = 2*self.atr_step -self.inter_atr_margin
                self.txt_atr_geometry = QRectF(0.0, 0.0, self.attribute_width / 2, self.attribute_height / 2)

            for i in range(0,self.no_atr):
                self.attach_attribute(QLineF(self.atr_step*i,0,self.atr_step*i,self.min_height - i*self.attribute_height),self.entity.attr_list[i].name,i,self.entity.attr_list[i].type,self.en_shape,self.attribute_width,self.attribute_height,self.txt_atr_geometry,-1)

                if(self.entity.attr_list[i].isComposite ):
                    no_child =len(self.entity.attr_list[i].attrib_childs)
                    if (no_child> 1):

                        ch_step = self.attribute_width / (len(self.entity.attr_list[0].attrib_childs) - 1)
                    else:
                        ch_step = self.attribute_width

                    par_x = self.atr_step*i - self.attribute_width / 2
                    par_y =self.min_height - i*self.attribute_height- self.attribute_height
                    for j in range(0,no_child):
                        self.attach_attribute(QLineF(par_x+(ch_step)*j,self.get_y_elipse(par_x+(ch_step)*j,par_x+self.attribute_width / 2,par_y+self.attribute_height/2),par_x+ch_step*j,par_y+self.min_height/2-j*self.attribute_height*0.75),self.entity.attr_list[i].attrib_childs[j].name,i,self.entity.attr_list[i].attrib_childs[j].type,self.en_shape,self.attribute_width*0.75,self.attribute_height*0.75,self.txt_atr_child_geometry,j)

                    child_height = -1*par_y-1*self.min_height+no_child*0.75*self.attribute_height
                    if(child_height>self.container_height):self.container_height=child_height


        elif( self.no_atr== 1):
            self.attach_attribute(QLineF(0,0,0,self.min_height),self.entity.attr_list[0].name,0,'prime',self.en_shape,self.attribute_width,self.attribute_height,self.txt_atr_geometry,-1)
            if (self.entity.attr_list[0].isComposite):
                no_child = len(self.entity.attr_list[0].attrib_childs)
                if(no_child > 1):

                     ch_step = self.attribute_width / (len(self.entity.attr_list[0].attrib_childs)-1)
                else:
                    ch_step = self.attribute_width

                par_x=0-self.attribute_width/2
                par_y=0+self.min_height-self.attribute_height

                for j in range(0, no_child):
                    self.attach_attribute(
                        QLineF(par_x+(ch_step) * j, self.get_y_elipse(par_x+(ch_step) * j,0,self.min_height-self.attribute_height/2), par_x+ch_step * j,par_y+ self.min_height / 2 - j * self.attribute_height *0.75),
                        self.entity.attr_list[0].attrib_childs[j].name, 0, self.entity.attr_list[0].attrib_childs[j].type,
                        self.en_shape, self.attribute_width *0.75, self.attribute_height *0.75,
                        self.txt_atr_child_geometry,j)
                    self.id += 1
                    self.container_height += self.attribute_height / 2 + -1*self.min_height / 2 - j * self.attribute_height / 2 + 10
                child_height = -1 * par_y - 1 * self.min_height + no_child * 0.75 * self.attribute_height
                if (child_height > self.container_height): self.container_height = child_height


    def attach_attribute(self,l,txt,id,type,parent,w,h,txt_geo,child):
        self.con_list.append (QGraphicsLineItem(parent))
        self.atr_shape_list.append( QGraphicsEllipseItem(parent))

        self.con_list[-1].setLine(l)
        self.con_list[-1].setPen(self.at_connection_pen)
        self.atr_shape_list[-1].setRect(QRectF(l.x1()-w/2,l.y2()-h,w,h))
        self.atr_shape_list[-1].setPen(self.attribute_pen)
        self.atr_shape_list[-1].setBrush(self.attribute_brush)

        self.atr_txt_list.append(self.scene.addWidget(QLineEdit()))
        self.atr_txt_list[-1].setParentItem(self.atr_shape_list[-1])
        self.atr_txt_list[-1].setGeometry(txt_geo)
        self.atr_txt_list[-1].widget().setFixedWidth(txt_geo.width())
        self.atr_txt_list[-1].widget().setFixedHeight(txt_geo.height())
        self.atr_txt_list[-1].widget().setStyleSheet(self.txt_style)

        if(type =='Prime'or type =='prime'):self.atr_txt_list[-1].widget().setStyleSheet('''QWidget{text-decoration:underline;font-weight:bold;}''')
        self.atr_txt_list[-1].setPos(l.x2()-self.txt_atr_geometry.width()/2,l.y2()-0.75*h)
        self.atr_txt_list [-1].widget().setText(txt)
        widget=self.atr_txt_list [-1].widget()
        self.atr_txt_list[-1].widget().editingFinished.connect( lambda :ContainerItem.trial(self,id,widget,child))
    def trial(self,id,widget,child):
        if id == -1:
            self.entity.name =widget.text()

        elif(child==-1) :
            self.entity.attr_list[id].name =widget.text()
        else:
            self.entity.attr_list[id].attrib_childs[child].name=widget.text()
    def connect_relation(self,x,y,type):
        ver_line = QGraphicsLineItem(self.en_shape)
        horz_line = QGraphicsLineItem(self.en_shape)
        ver_line.setLine(QLineF(self.rel_orgn.x(),self.rel_orgn.y(),self.rel_orgn.x(),y-self.en_shape.y()))
        horz_line.setLine(QLineF(ver_line.line().x2(), ver_line.line().y2() ,x-self.en_shape.x() ,y-self.en_shape.y()))

        self.rel_orgn.setX(self.rel_orgn.x()+self.orgn_step)
        if(type =='p'):
            ver_line.setPen(QPen(Qt.black,3,Qt.DashLine))
            horz_line.setPen(QPen(Qt.black, 3, Qt.DashLine))
    def get_y_elipse(self,x,h,k):
        a=(self.attribute_width/2)
        b=self.attribute_height/2
        m =((x-h)**2)/a**2
        return (((1-m)*b**2)**0.5*-1)+k








class view(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.title = "mainWindow"
        self.top   = 0
        self.left = 0
        self.width = 1400
        self.height =800
        self.scene  =QGraphicsScene(0,0,self.width,self.height)
        self.container_margin = 120
        self.container_max_height = 0
        self.rel_width = 70*2
        self.rel_height = 40*2
        self.r_atr_h=30
        self.r_atr_w=80
        self.r_atr_line=50
        self.rel_pen = QPen(Qt.black,3,Qt.SolidLine)
        self.rel_Brush = QBrush(QColor(255,204,153), Qt.SolidPattern)
        self.level = 100
        # self.setBackgroundBrush(QBrush(Qt.darkGray,Qt.CrossPattern))
        self.InitWindow()

    def InitWindow(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)
            self.setScene(self.scene)
            self. setDragMode(QGraphicsView.ScrollHandDrag)
            self.setRenderHint(QPainter.Antialiasing)
            self.setRenderHint(QPainter.TextAntialiasing)


    def add_Ens(self,e_list):
        self.item_list = []
        self.data = e_list

        for i in range(0,len(e_list)):
            self.item_list.append(ContainerItem(e_list[i],QPointF(500,500),self.scene))
            if self.item_list[-1].container_height>self.container_max_height:
                self.container_max_height = self.item_list[-1].container_height
        cur_x = self.item_list[0].attribute_width/2
        cur_y = self.container_max_height
        self.level =cur_y + self.item_list[0].entity_height+self.rel_height
        for j in range(0,len(self.item_list)):
            self.item_list[j].en_shape.setPos(cur_x,cur_y)
            cur_x += self.item_list[0].container_width +self.container_margin
            if(cur_x + self.item_list[0].container_width>self.scene.width()):
                self.width += self.item_list[0].container_width
                self.scene.setSceneRect(QRectF(0,0,self.width,self.height))
                # self.gen.widget().setGeometry(self.width-self.gen.widget().width(), self.height-self.gen.widget().height(), self.gen.widget().width(), self.gen.widget().height())
        for k in range(0,len(e_list)):
            for n in range(0,len(e_list[k].relations)):
                if(self.get_index(e_list[k].relations[n].getTargetEntity(e_list[k]))>=k):
                    start =self.item_list[k].en_shape.x()+self.item_list[k].entity_width
                    self.add_relation(start,e_list[k].relations[n])
                    self.item_list[k].connect_relation(start,self.level,e_list[k].relations [n].p_type1)

                    self.item_list[self.get_index (e_list[k].relations[n].getTargetEntity(e_list[k]))].connect_relation(start+self.rel_width,self.level,e_list[k].relations[n].p_type1)
                    self.level+=self.rel_height+10
                    if (self.level + self.rel_height / 2 >= self.scene.height()):
                        self.height = self.level + self.rel_height / 2
                        self.scene.setSceneRect(QRectF(0, 0, self.width, self.height))

    def get_data(self):
        return self.data


    def add_relation(self,x,r):
        if (len(r.attrib_list)!=0):self.level+=self.rel_height/2+self.r_atr_h*(len(r.attrib_list)-1)+self.r_atr_line

        Qpoints =  [
            QPointF(x,self.level),
            QPointF(x+self.rel_width/2,self.level + self.rel_height/2),
            QPointF(x+self.rel_width,self.level),
            QPointF(x+self.rel_width/2,self.level-self.rel_height/2)

        ]
        rel_shape=self.scene.addPolygon(QPolygonF(Qpoints),self.rel_pen,self.rel_Brush)
        rel_name = self.scene.addWidget(QLineEdit())
        left_p = self.scene.addWidget(QLineEdit())
        right_p = self.scene.addWidget(QLineEdit())
        #rel_name.setParentItem(rel_shape)
        rel_name.setGeometry(QRectF(0,0,self.rel_width/2,3))
        left_p.setGeometry(QRectF(0,0,0,0))
        right_p.setGeometry(QRectF(0, 0, 0, 0))
        left_p.widget().setFixedWidth(43)
        right_p.widget().setFixedWidth(43)
        rel_name.setPos(x+self.rel_width/4,self.level-rel_name.widget().height()/2)
        left_p.setPos(x-left_p.widget().width(), self.level-left_p.widget().height())
        right_p.setPos(x +self.rel_width, self.level-right_p.widget().height())
        rel_name.widget().setText(r.name)
        left_p.widget().setText(r.p_ratio1)
        right_p.widget().setText(r.p_ratio2)
        rel_name.widget().editingFinished.connect( partial(self.mod,"n",r,rel_name.widget()))
        left_p.widget().editingFinished.connect(partial(self.mod,"l",r,left_p.widget()))
        right_p.widget().editingFinished.connect(partial(self.mod,"r",r,right_p.widget()))
        atr_step =  ((self.rel_width-2*right_p.widget().width()-10)/ (len(r.attrib_list) -1))if len(r.attrib_list) > 1 else 0
        ten=(Qpoints[0].y()-Qpoints[3].y())/(Qpoints[0].x()-Qpoints[3].x())
        for i in range(len(r.attrib_list)):
            first_pt=QPointF(Qpoints[0].x()+i*atr_step+right_p.widget().width()+10,self.get_y_line(Qpoints[0].x()+i*atr_step+right_p.widget().width()+10,Qpoints[0],ten))
            if(first_pt.x()>Qpoints[3].x()):first_pt.setY(self.get_y_line(first_pt.x(),Qpoints[3],-1*ten))

            atr_line=self.scene.addLine(first_pt.x(),first_pt.y(),first_pt.x(),Qpoints[3].y() -self.r_atr_line-i*self.r_atr_h)
            elip_pt = QPointF(first_pt.x()-self.r_atr_w/2, atr_line.line().y2() - self.r_atr_h )
            atr_elipse =self.scene.addEllipse(QRectF(0,0,self.r_atr_w,self.r_atr_h),self.rel_pen,self.rel_Brush)
            txt=[]
            txt.append(self.scene.addWidget(QLineEdit(r.attrib_list[i].name)))
            atr_elipse.setPos(elip_pt)
            txt[-1] .setPos(elip_pt.x()+self.rel_width*0.25,elip_pt.y()+self.r_atr_h*0.125 )
            txt[-1] .widget().setFixedWidth(self.r_atr_w*0.5)
            txt[-1] .widget().setFixedHeight(self.r_atr_h * 0.75)
            txt[-1] .widget().editingFinished.connect(partial(self.mod,"c",r,txt[-1].widget(),i))


    def get_y_line(self,x,p1,ten):
        return (x-p1.x())*ten+p1.y()
    def get_index (self,id):
        for i in range(0,len(self.item_list)):
            if(id == self.item_list[i].entity.id):
                return i
    def mod(self,type,r,w,child=-1):
        if type =="n" :
            r.name = w.text()
        elif type=='l':
            r.p_ratio1 = w.text()
        elif type=='r':
            r.p_ratio2 = w.text()
        elif type=='c':
            r.attrib_list[child].name = w.text()


class main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(0,0,1000,500)
        self.but = QPushButton("",self)
        self.but_width=100
        self.but_height=100
        self.but.setGeometry(self.width()/2-self.but_width/2,self.height()/2-self.but_height/2,self.but_width,self.but_height)
        self.icon =QIcon(QPixmap("Icons/add.jpeg").scaled(self.but_width,self.but_height))
        self.but.setIcon(self.icon)
        self.but.setIconSize(QSize(self.but_width/2,self.but_height/2))
        self.but.clicked.connect(self.get_file)
        self.setWindowTitle("DataBase Helper")
        self.show()
    def get_file(self):
        self.file_name = QFileDialog().getOpenFileName(caption="choose imag",filter="Image Files (*.png *.jpg *.bmp)")
        print(self.file_name[0])
        img =cv2.imread(self.file_name[0])
        en_l =image.ERD_Project(img)
        print(len(en_l[0].relations[0].attrib_list))
        self.second_window = second_window(en_l)

class second_window(QMainWindow):
    def  __init__(self,en_list):
        QMainWindow.__init__(self)
        self.width = 1400
        self.height =800
        self.setGeometry(0,0,self.width,self.height)
        self.gen = QPushButton("Generate Sql",self)
        self.gen.clicked.connect(self.generate_sql)
        self.imp = QPushButton("implement",self)
        self.imp.clicked.connect(self.show_dial)

        self.editor =view()
        self.editor.setParent(self)
        self.gen.setGeometry(self.width , self.height ,
        self.gen.width(), self.gen.height())
        self.imp.setGeometry(self.width-self.gen.width()-20 ,self.height,self.imp.width(),self.imp.height())
        self.editor.add_Ens(en_list)
        self.show()

    def generate_sql(self):
        self.file = QFileDialog().getSaveFileName(caption="save")[0]
        Gui_interface.create_SQL(self.editor.data,"localhost","root","",path=self.file)
    def show_dial(self):
        info=sql_info(self.editor.data,self)
        info.exec_()
class sql_info(QDialog):
    def __init__(self,en,parent):
        super().__init__()



        self.en =en
        self.lay = QGridLayout()
        self.setLayout(self.lay)


        self.labels = ["database-name *","username *","password"]
        self.defaults = ["db1","root",""]
        self.input  =[]
        self.crt = QPushButton("create",self)

        for row in range (3):

            self.lay.addWidget(QLabel(self.labels[row]),row,0)
            self.input .append(QLineEdit(self.defaults[row]))
            self.lay.addWidget(self.input[row],row,1)
        self.crt.setGeometry(self.width(),self.height(),self.crt.width(),self.crt.height())
        self.lay.addWidget(self.crt,3,1)
        self.input[2].setEchoMode(QLineEdit.Password)
        self.crt.clicked.connect(self.create)

    def create(self):
        data= []
        for i in range(2):
            if(self.input[i].text()==""):
                self.err=QMessageBox(text="please fill all required fields with *")
                self.err.show()
                return
        self.setVisible(False)
        Gui_interface.create_SQL(self.en,self.input[0].text(),self.input[1].text(),self.input[2].text(),implementation=True)



app =QApplication(sys.argv)
myWindow = main()
# # myWindow.add_pushButton()
# myWindow.InitWindow()
# myWindow.show()
# second = second_window()
# second.show()


app.exec()



