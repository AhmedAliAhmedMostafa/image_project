import cv2
import numpy as np
from matplotlib import pyplot as plt


kernel = np.ones((1,1),np.uint8)

image = cv2.imread('/Users/ahmednasser/Downloads/flowchart.png')   #read the image
#cv2.imshow('Original image', image)
# converting the image to gray scale

def rgb2gray(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

gray = rgb2gray(image)
#show the images
#cv2.imshow('Gray image', gray)

#gaussian filter

# Median filter function provided by OpenCV. ksize is the kernel size.
def medain(grayImage,ksize=3 ):

    img = cv2.medianBlur(grayImage, ksize)
    return img

filtred_gray_image = medain(gray)
#cv2.imshow('gaussaan filter', filtred_gray_image)

#this step is for binary (bitwise inversion )

def  binaryImage (blackAndWhiteImage):
    (thresh, blackAndWhiteImage) = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    return  blackAndWhiteImage

blackAndWhite_image = binaryImage(filtred_gray_image)
#cv2.imshow('Black white image', blackAndWhite_image)

#invert the blackAndWhitecolor
def invert (blackAndWhite):
    blackAndWhite= (255-blackAndWhite)
    return  blackAndWhite

inverted_image = invert(blackAndWhite_image)
#cv2.imshow('inverted image',inverted_image)

#filter the inverted image
def invertedImageFiltering (invertedImage):
    opening = cv2.morphologyEx(invertedImage, cv2.MORPH_OPEN, kernel)
    return  opening

filtered_inverted_image = invertedImageFiltering(inverted_image)
cv2.imshow('filtered_inverted_image',filtered_inverted_image)

#hough transformer ---- first step is edge  detection
def edgeDetection (filterdInvImg):
    edges = cv2.Canny(filterdInvImg,100,200)
    return edges

edge_detection_image = edgeDetection(filtered_inverted_image)
cv2.imshow('edges images', edge_detection_image)





cv2.waitKey(0)
cv2.destroyAllWindows()