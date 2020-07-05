import math
import cv2
import numpy as np

def encCirc(imagen, thres=130, blur=5, contMin=100, contMax=320, cMin=0.6, cMax=1.2, grosor=1, color=(255,0,0)):
    """
    Inputs: 
        img -> imagen de entrada,
        thres -> umbral de threshold
        blur -> filtro gaussiano
        contMin -> area mínima
        contMax -> area máxima
        cMin -> circularidad mínima
        cMax -> circularidad máxima
        grosor -> grosor de los circulos en la imagen de salida
    Outputs:
        contours_area -> contornos que cumplen con las áreas de salida
        contour_circles -> contornos que cumplen con los criterios de circularidad
        centro -> lista de centros de los circulos
        radio -> lista de radios de los circulos
    """
    contours_area = []
    contours_circles = []
    radio=[]
    centro=[]
    imgray=imagen
    #imgray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    im_gauss = cv2.GaussianBlur(imgray, (blur, blur), 0)
    ret, imgthresh = cv2.threshold(im_gauss, thres,255, cv2.THRESH_BINARY_INV)
    #print(ret)
    #cv2.imshow("thhreshold", imgthresh)
    if ret!=0:
        contours, hierarchy = cv2.findContours(imgthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for con in contours:
            area = cv2.contourArea(con)
            perimeter = cv2.arcLength(con, True)
            if perimeter == 0:
                break
            circularity = 4*math.pi*(area/(perimeter*perimeter))
            if contMin < area < contMax:
                contours_area.append(con)
                if cMin < circularity < cMax:
                    contours_circles.append(con)
                    centro1, radio1=cv2.minEnclosingCircle(con)
                    centro.append([int(centro1[0]), int(centro1[1])])
                    radio.append(int(radio1))
    cv2.drawContours(imagen, contours_circles, -1, color, grosor)
    return contours_area, contours_circles, centro, radio

