import numpy as np
import cv2
import math
from Data_structure import Entity as Shapes

Entities = []
Relations = []
Attributes = []
Lines = []



def fillHole(im_in):
    im_floodfill = im_in.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h1, w1 = im_in.shape[:2]
    mask = np.zeros((h1 + 2, w1 + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_in | im_floodfill_inv

    return im_out

def GetLines(onlyline1, img):
    lines = cv2.HoughLinesP(onlyline1, 1, np.pi / 180, 38, None, minLineLength=0, maxLineGap=10)
    print(len(lines))
    numberoflines = 0
    for line in lines:
        numberoflines = numberoflines + 1
        xL, yL, x2, y2 = line[0]
        cv2.line(img, (xL, yL), (x2, y2), (255, 0, 255), 2)
        StartP = Shapes.point(xL, yL)
        EndP = Shapes.point(x2, y2)
        li = Shapes.lineobj("Line" + str(numberoflines), "undefined", StartP, EndP)
        Lines.append(li)
        cv2.putText(img, "line", (int(xL), int(yL)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    return img


def GetShapes (opening1, img):
    contours, _ = cv2.findContours(opening1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    numberofent = 0
    numberofrel = 0
    numberofatt = 0
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5

        if len(approx) == 4:
            x1, y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w) / h
            apratio = cv2.contourArea(contour) / (w * h)
            # print(aspectRatio)
            if 0.95 <= aspectRatio <= 1.05 or apratio < 0.73:
                numberofrel = numberofrel + 1
                print("Squares", len(approx))
                print("aspectRatio", aspectRatio)
                cv2.putText(img, "Rel" + str(numberofrel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                CeP = Shapes.point(cX, cY)
                rel = Shapes.relation("Rel" + str(numberofrel), -1, -1, "undefined", "undefined", "undefined", "undefined",
                               CeP)
                Relations.append(rel)

                # draw the contour and center of the shape on the image
                # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(img, (cX, cY), 5, (0, 255, 255), -1)
            elif cv2.contourArea(contour) > 1000:
                numberofent = numberofent + 1
                print("Rectangle", len(approx))
                print("aspectRatio", aspectRatio)
                cv2.putText(img, "Ent" + str(numberofent - 1), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                CentP = Shapes.point(cX, cY)
                # draw the contour and center of the shape on the image
                # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(img, (cX, cY), 5, (0, 255, 255), -1)
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
                ent = Shapes.entity("Ent" + str(numberofent - 1), CentP)
                Entities.append(ent)

        elif 4 <= len(approx) < 7 and cv2.contourArea(contour) > 100:
            print("Squares", len(approx))
            numberofrel = numberofrel + 1
            # print("aspectRatio", aspectRatio)
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            CeP1 = Shapes.point(cX, cY)
            # draw the contour and center of the shape on the image
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(img, (cX, cY), 5, (0, 255, 255), -1)
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
            cv2.putText(img, "Rel" + str(numberofrel) + str(numberofrel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            rel = Shapes.relation("Rel" + str(numberofrel), -1, -1, "undefined", "undefined", "undefined", "undefined", CeP1)
            Relations.append(rel)
        elif len(approx) > 6:
            print("Cirlcles", len(approx))
            numberofatt = numberofatt + 1
            cv2.putText(img, "Att" + str(numberofatt), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            cv2.drawContours(img, [approx], 0, (255, 0, 0), 2)
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            CirCentP = Shapes.point(cX, cY)
            # draw the contour and center of the shape on the image
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(img, (cX, cY), 5, (0, 255, 255), -1)
            att = Shapes.attribute("Att" + str(numberofatt), "undefined", CirCentP)
            Attributes.append(att)

    return img


def drawShapes(img):
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Denoise = cv2.medianBlur(imgGrey, 3)
    #cv2.imshow("imgGrey", Denoise)

    _, thrash = cv2.threshold(imgGrey, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow("Thresh", thrash)

    binaryconverted = (255 - thrash)
    cv2.imshow("binaryconverted", binaryconverted)

    binaryconverted1 = fillHole(binaryconverted)
    cv2.imshow("binaryconverted1", binaryconverted1)

    binaryconverted1 = cv2.erode(binaryconverted1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    opening = cv2.morphologyEx(binaryconverted1, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    opening1 = cv2.medianBlur(opening, 3)
    cv2.imshow("opening1", opening1)

    opening2 = cv2.dilate(opening, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    #cv2.imshow("opening2", opening2)

    closing = cv2.morphologyEx(binaryconverted1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
    #cv2.imshow("closing", closing)

    onlyline1 = binaryconverted1 - opening1
    onlyline1 = cv2.medianBlur(onlyline1, 3)
    onlyline1 = cv2.erode(onlyline1, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1)))
    cv2.imshow("onlyline1", onlyline1)

    onlyline2 = binaryconverted1 - opening2
    #cv2.imshow("onlyline2", onlyline2)

    #edges = cv2.Canny(onlyline2, 150, 400, None, 3)
    #cv2.imshow("edges", edges)

    imgLine = GetLines(onlyline1, img)
    #cv2.imshow("DrawOnlyLine", imgLine)

    shapesImage = GetShapes(opening1, img)
    cv2.imshow("shapesImage", shapesImage)

    return img


def CalcDistance(Point1, Point2):
    return math.sqrt(math.pow(Point1.x - Point2.x, 2) + math.pow(Point1.y - Point2.y, 2))


def ConnectedSh(line, Ents, Attrs, Rels):
    startPointofLine = line.StartPoint
    endPointofLine = line.EndPoint
    connectedtostart = Ents[0].name
    connectedtoend = Ents[0].name

    MinDisSt = CalcDistance(startPointofLine, Ents[0].CenPoint)
    for i in range(1, len(Ents)):
        MinDisTemp = CalcDistance(startPointofLine, Ents[i].CenPoint)
        if MinDisTemp < MinDisSt:
            MinDisSt = MinDisTemp
            connectedtostart = Ents[i].name

    for i1 in range(0, len(Attrs)):
        MinDisTemp = CalcDistance(startPointofLine, Attrs[i1].CenPoint)
        if MinDisTemp < MinDisSt:
            MinDisSt = MinDisTemp
            connectedtostart = Attrs[i1].name
    for i2 in range(0, len(Rels)):
        MinDisTemp = CalcDistance(startPointofLine, Rels[i2].CenPoint)
        if MinDisTemp < MinDisSt:
            MinDisSt = MinDisTemp
            connectedtostart = Rels[i2].name

    MinDisEnd = CalcDistance(endPointofLine, Ents[0].CenPoint)
    for i3 in range(0, len(Ents)):
        MinDisTemp = CalcDistance(endPointofLine, Ents[i3].CenPoint)
        if MinDisTemp < MinDisEnd:
            MinDisEnd = MinDisTemp
            connectedtoend = Ents[i3].name

    for i4 in range(0, len(Attrs)):
        MinDisTemp = CalcDistance(endPointofLine, Attrs[i4].CenPoint)
        if MinDisTemp < MinDisEnd:
            MinDisEnd = MinDisTemp
            connectedtoend = Attrs[i4].name
    for i5 in range(0, len(Rels)):
        MinDisTemp = CalcDistance(endPointofLine, Rels[i5].CenPoint)
        if MinDisTemp < MinDisEnd:
            MinDisEnd = MinDisTemp
            connectedtoend = Rels[i5].name

    connectedshape = [connectedtostart, connectedtoend]
    return connectedshape


def unique(list1):
    ConUniq = []
    for h in range(1, len(list1)):
        if list1[h][0] != list1[h][1]:
            ConUniq.append(list1[h])
            break

    for i in range(1, len(list1)):
        b = True
        for j in range(0, len(ConUniq)):
            str = list1[i][0]
            if (str == ConUniq[j][0] and list1[i][1] == ConUniq[j][1]) \
                    or (list1[i][0] == ConUniq[j][1] and list1[i][1] == ConUniq[j][0]) \
                    or(list1[i][1] == ConUniq[j][0] and list1[i][0] == ConUniq[j][1]) \
                    or (list1[i][0] == list1[i][1]):
                b = False
                break
        if b == True:
            ConUniq.append(list1[i])


    return ConUniq
    
    
def Merge(lines, Ents, Attrs, Rels):
    connectedshapes = []
    for i in range(0, len(lines)):
        connectedshapes.append(ConnectedSh(lines[i], Ents, Attrs, Rels))

    Uniqconnectedshapes=unique(connectedshapes)

    for i in range(0, len(Uniqconnectedshapes)):
        if "Ent" in Uniqconnectedshapes[i][0] and "Rel" in Uniqconnectedshapes[i][1]:
            stri1 = Uniqconnectedshapes[i][0]
            stri2 = Uniqconnectedshapes[i][1]
            if Relations[int(stri2[len(stri2)-1:]) - 1].id1 == -1:
                id1 = Entities[int(stri1[len(stri1)-1:])].getID()
                Relations[int(stri2[len(stri2)-1:]) - 1].id1 = id1
                Entities[int(stri1[len(stri1) - 1:])].add_relation(Relations[int(stri2[len(stri2)-1:]) - 1])
            elif Relations[int(stri2[len(stri2) - 1:]) - 1].id2 == -1:
                id2 = Entities[int(stri1[len(stri1)-1:])].getID()
                Relations[int(stri2[len(stri2)-1:]) - 1].id2 = id2
                Entities[int(stri1[len(stri1) - 1:])].add_relation(Relations[int(stri2[len(stri2)-1:]) - 1])
                Relations[int(stri2[len(stri2) - 1:]) - 1].id = Relations[int(stri2[len(stri2)-1:]) - 1].id1 ^ id2

        elif "Rel" in Uniqconnectedshapes[i][0] and "Ent" in Uniqconnectedshapes[i][1]:
            stri1 = Uniqconnectedshapes[i][1]
            stri2 = Uniqconnectedshapes[i][0]
            index = stri2[len(stri2)-1:]
            if Relations[int(index) - 1].id1 == -1:
                id1 = Entities[int(stri1[len(stri1) - 1:])].getID()
                Relations[int(stri2[len(stri2)-1:]) - 1].id1 = id1
                Entities[int(stri1[len(stri1) - 1:])].add_relation(Relations[int(stri2[len(stri2) - 1:]) - 1])
            elif Relations[int(stri2[len(stri2) - 1:]) - 1].id2 == -1:
                id2 = Entities[int(stri1[len(stri1) - 1:])].getID()
                Relations[int(stri2[len(stri2) - 1:]) - 1].id2 = id2
                Entities[int(stri1[len(stri1) - 1:])].add_relation(Relations[int(stri2[len(stri2) - 1:]) - 1])
                Relations[int(stri2[len(stri2) - 1:]) - 1].id = Relations[int(stri2[len(stri2)-1:]) - 1].id1 ^ id2


        elif "Ent" in Uniqconnectedshapes[i][0] and "Att" in Uniqconnectedshapes[i][1]:
            stri1 = Uniqconnectedshapes[i][0]
            stri2 = Uniqconnectedshapes[i][1]
            Entities[int(stri1[len(stri1)-1:])].add_attr(Attributes[int(stri2[len(stri2)-1:]) - 1])
            Attributes[int(stri2[len(stri2) - 1:]) - 1].isParent = True

        elif "Att" in Uniqconnectedshapes[i][0] and "Ent" in Uniqconnectedshapes[i][1]:
            stri2 = Uniqconnectedshapes[i][0]
            stri1 = Uniqconnectedshapes[i][1]
            Entities[int(stri1[len(stri1)-1:])].add_attr(Attributes[int(stri2[len(stri2)-1:]) - 1])
            Attributes[int(stri2[len(stri2) - 1:]) - 1].isParent = True

        elif "Att" in Uniqconnectedshapes[i][0] and "Rel" in Uniqconnectedshapes[i][1]:
            stri1 = Uniqconnectedshapes[i][0]
            stri2 = Uniqconnectedshapes[i][1]
            Relations[int(stri2[len(stri2)-1:]) - 1].add_attrib(Attributes[int(stri1[len(stri1)-1:]) - 1])
            Attributes[int(stri1[len(stri1) - 1:]) - 1].isParent = True

        elif "Rel" in Uniqconnectedshapes[i][0] and "Att" in Uniqconnectedshapes[i][1]:
            stri2 = Uniqconnectedshapes[i][0]
            stri1 = Uniqconnectedshapes[i][1]
            Relations[int(stri2[len(stri2)-1:]) - 1].add_attrib(Attributes[int(stri1[len(stri1)-1:]) - 1])
            Attributes[int(stri1[len(stri1) - 1:]) - 1].isParent = True

    # Merge Composite Attribute
    for i in range(0, len(Uniqconnectedshapes)):
        if "Att" in Uniqconnectedshapes[i][0] and "Att" in Uniqconnectedshapes[i][1]:
            stri1 = Uniqconnectedshapes[i][0]
            stri2 = Uniqconnectedshapes[i][1]
            if Attributes[int(stri1[len(stri1) - 1:]) - 1].isParent:
                Attributes[int(stri1[len(stri1) - 1:]) - 1].isComposite = True
                Attributes[int(stri1[len(stri1) - 1:]) - 1].add_child(Attributes[int(stri2[len(stri2) - 1:]) - 1])
            elif Attributes[int(stri2[len(stri2) - 1:]) - 1].isParent:
                Attributes[int(stri2[len(stri2) - 1:]) - 1].isComposite = True
                Attributes[int(stri2[len(stri2) - 1:]) - 1].add_child(Attributes[int(stri1[len(stri1) - 1:]) - 1])

    return Uniqconnectedshapes


img = cv2.imread('\ASU\Senior\Flowchart10.png')
cv2.imshow("img", img)
Test = drawShapes(img)
Test2 = Merge(Lines, Entities, Attributes, Relations)

print("Smile", Test2)
# contours1, _ = cv2.findContours(onlyline, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# for contour1 in contours1:
# approx1 = cv2.approxPolyDP(contour1, 0.001 * cv2.arcLength(contour1, True), False)
# cv2.drawContours(img, [approx1], 0, (0, 0, 255), 2)
# x1 = approx1.ravel()[0]
# y1 = approx1.ravel()[1]
# print(len(approx1))
# cv2.putText(img, "line", (int(x1), int(y1)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


# Exiting the window if 'q' is pressed on the keyboard.
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
