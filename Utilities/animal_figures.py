import cv2
import numpy as np
import math

def limit(number):
    if number>150:
        number=number*0.5
    else:
        number=number*0.6
    return number

def change_month(list,mounth_shape):
    if list[0]-list[1]<160  :
        mounth_shape=int(mounth_shape*0.3)
    else:
        mounth_shape=int(mounth_shape)
    return mounth_shape
def eating(list,color):
    if list[0]-list[1]<160    :
        color=(0,0,255)
    else:
        color=color
    return color
def draw_rabbit(list,img):
    color_head=(128,84,231)
    color_out=(0,0,0)
    color_inside=(255,255,255)
    x=[ list[x][1] for x in range(len(list)) ]
    y=[ list[x][2] for x in range(len(list)) ]
    mountion=y[0],y[12]
    cx,cy=int(np.average(x)+np.average(x)*0.02),int(np.average(y)+np.average(y)*0.031)
    leng=int(math.hypot(x[8] - x[0],y[8] - y[0])*0.65)
    size=limit(leng)
    head_size=int(size*0.95)
    eye_size=int(head_size*0.2)
    center_coordinate=cx,cy
    right_eye_coor=center_coordinate[0]+int(size*0.3),center_coordinate[1]-int(size*0.2)
    left_eye_coor=center_coordinate[0]-int(size*0.3),center_coordinate[1]-int(size*0.2)
    mounth_rabbit_center=center_coordinate[0],center_coordinate[1]+int(size*0.40)
    noise_center=center_coordinate[0],center_coordinate[1]+int(size*0.2)
    mounth_shape=int(size*0.3)
    right_ear_coor=center_coordinate[0]+int(size*0.3),center_coordinate[1]-int(size*1.3)
    left_ear_coor=center_coordinate[0]-int(size*0.4),center_coordinate[1]-int(size*1.3)
    cv2.circle(img,center_coordinate,int(size),color_head,cv2.FILLED)
    cv2.circle(img,right_eye_coor,eye_size,color_out,cv2.FILLED)
    cv2.circle(img,right_eye_coor,int(eye_size*0.8),color_inside,cv2.FILLED)
    cv2.circle(img,right_eye_coor,int(eye_size*0.3),color_out,cv2.FILLED)
    cv2.circle(img,left_eye_coor,eye_size,color_out,cv2.FILLED)
    cv2.circle(img,left_eye_coor,int(eye_size*0.8),color_inside,cv2.FILLED)
    cv2.circle(img,left_eye_coor,int(eye_size*0.3),color_out,cv2.FILLED)
    cv2.circle(img,noise_center,int(eye_size*0.8),color_out,cv2.FILLED)
    cv2.ellipse(img,mounth_rabbit_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.6)),0,0,180,color_out,-1)
    cv2.ellipse(img,mounth_rabbit_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.5)),0,0,180,eating(mountion,color_inside),-1)
    cv2.ellipse(img,right_ear_coor,(int(int(size*0.3)*1.9),int(int(size*0.3)*0.6)),92,0,360,color_head,-1)
    cv2.ellipse(img,left_ear_coor,(int(int(size*0.3)*1.9),int(int(size*0.3)*0.6)),50,0,360,color_head,-1)
    return img
def draw_dog(list,img):
    color_out=(0,0,0)
    color_inside=(255,255,255)
    color_head=(33,67,101)
    color_eye_out=(0,0,0)
    color_eye_inside=(255,255,255)
    x=[ list[x][1] for x in range(len(list)) ]
    y=[ list[x][2] for x in range(len(list)) ]

    mountion=y[0],y[12]
    cx,cy=int(np.average(x)+np.average(x)*0.02),int(np.average(y)+np.average(y)*0.031)
    leng=int(math.hypot(x[8] - x[0],y[8] - y[0])*0.65)
    size=limit(leng)
    head_size=int(size*0.95)
    eye_size=int(head_size*0.2)
    center_coordinate=cx,cy
    right_eye_coor=center_coordinate[0]+int(size*0.3),center_coordinate[1]-int(size*0.2)
    left_eye_coor=center_coordinate[0]-int(size*0.3),center_coordinate[1]-int(size*0.2)
    mounth_center=center_coordinate[0],center_coordinate[1]+int(size*0.40)
    noise_center=center_coordinate[0],center_coordinate[1]+int(size*0.2)
    mounth_shape=int(size*0.3)
    right_ear_coor=center_coordinate[0]+int(size*0.3),center_coordinate[1]-int(size*0.6)
    left_ear_coor=center_coordinate[0]-int(size*0.4),center_coordinate[1]-int(size*0.6)
    cv2.ellipse(img,center_coordinate,(head_size,int(head_size*0.9)),0,0,360,color_head,cv2.FILLED)
    cv2.ellipse(img,right_ear_coor,(int(int(size*0.3)*1.9),int(size*0.2)),130,0,360,color_head,-1)
    cv2.ellipse(img,left_ear_coor,(int(int(size*0.3)*1.9),int(size*0.2)),50,0,360,color_head,-1)
    cv2.circle(img,right_eye_coor,eye_size,color_out,cv2.FILLED)
    cv2.circle(img,right_eye_coor,int(eye_size*0.8),color_inside,cv2.FILLED)
    cv2.circle(img,right_eye_coor,int(eye_size*0.3),color_out,cv2.FILLED)
    cv2.circle(img,left_eye_coor,eye_size,color_out,cv2.FILLED)
    cv2.circle(img,left_eye_coor,int(eye_size*0.8),color_inside,cv2.FILLED)
    cv2.circle(img,left_eye_coor,int(eye_size*0.3),color_out,cv2.FILLED)
    cv2.circle(img,noise_center,int(eye_size*0.8),color_out,cv2.FILLED)
    cv2.circle(img,noise_center,int(eye_size*0.3),color_inside,cv2.FILLED)
    cv2.line(img,noise_center,(noise_center[0]+int(head_size*0.3),noise_center[1]),color_out,2)
    cv2.line(img,noise_center,(noise_center[0]+int(head_size*0.3),noise_center[1]+int(head_size*0.1)),color_out,2)
    cv2.line(img,noise_center,(noise_center[0]-int(head_size*0.3),noise_center[1]),color_out,2)
    cv2.line(img,noise_center,(noise_center[0]-int(head_size*0.3),noise_center[1]+int(head_size*0.1)),color_out,2)
    cv2.circle(img,noise_center,int(eye_size*0.3),color_inside,cv2.FILLED)
    cv2.ellipse(img,mounth_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.6)),0,0,180,color_out,-1)
    cv2.ellipse(img,mounth_center,(int(change_month(mountion,mounth_shape)*1.1),int(change_month(mountion,mounth_shape)*0.7)),0,0,180,eating(mountion,color_inside),-1)

    return img
def draw_fish(list,img):
    color_out=(0,0,0)
    color_inside=(255,255,255)
    color=(255,255,0)
    color_eye_out=(0,0,0)
    color_eye_inside=(255,255,255)
    x=[ list[x][1] for x in range(len(list)) ]
    y=[ list[x][2] for x in range(len(list)) ]
    mountion=y[0],y[12]
    cx,cy=int(np.average(x)+np.average(x)*0.02),int(np.average(y)+np.average(y)*0.031)
    leng=int(math.hypot(x[8] - x[0],y[8] - y[0])*0.65)
    size=limit(leng)
    head_size=int(size*0.95)
    eye_size=int(head_size*0.2)
    center_coordinate=cx,cy
    body_size=int(size*1.4)
    eye_size=int(body_size*0.081)
    mounth_shape=int(head_size*0.3)
    mounth_center=center_coordinate[0]-int(head_size*0.50),center_coordinate[1]-int(head_size*0.5)
    eye_coor=center_coordinate[0]-int(head_size*0.50),center_coordinate[1]-int(head_size*0.8)
    tail_coor_upp=center_coordinate[0]+int(head_size),center_coordinate[1]+int(head_size*1.1)
    tail_coor_down=center_coordinate[0]+int(head_size*0.8),center_coordinate[1]+int(head_size*1.2)
    pad_coor=center_coordinate[0]+int(body_size*0.33),center_coordinate[1]-int(body_size*0.12)
    cv2.ellipse(img,center_coordinate,(body_size,int(body_size*0.41)),60,0,360,color,-1)
    cv2.circle(img,eye_coor,eye_size,color_eye_out,cv2.FILLED)
    cv2.circle(img,eye_coor,int(eye_size*0.8),color_eye_inside,cv2.FILLED)
    cv2.circle(img,eye_coor,int(eye_size*0.3),color_eye_out,cv2.FILLED)
    cv2.ellipse(img,pad_coor,(int(size*0.44),int(size*0.4)),-20,180,360,color,-1)
    cv2.ellipse(img,tail_coor_upp,(int(size*0.22),int(size*0.60)),110,0,360,color,-1)
    cv2.ellipse(img,tail_coor_down,(int(size*0.22),int(size*0.60)),-20,0,360,color,-1)
    cv2.ellipse(img,mounth_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.6)),30,0,180,color_out,-1)
    cv2.ellipse(img,mounth_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.5)),30,0,180,eating(mountion,color_inside),-1)
    return img
def draw_angry_dog(list,img):
    color_out=(0,0,0)
    color_inside=(255,255,255)
    color_head=(33,67,101)
    color_eye_out=(0,0,0)
    color_eye_inside=(255,255,255)
    x=[ list[x][1] for x in range(len(list)) ]
    y=[ list[x][2] for x in range(len(list)) ]
    mountion=y[0],y[12]
    cx,cy=int(np.average(x)+np.average(x)*0.02),int(np.average(y)+np.average(y)*0.031)
    leng=int(math.hypot(x[8] - x[0],y[8] - y[0])*0.65)
    size=limit(leng)
    head_size=int(size*0.95)
    eye_size=int(head_size*0.2)
    center_coordinate=cx,cy
    right_eye_coor=center_coordinate[0]+int(size*0.3),center_coordinate[1]-int(size*0.2)
    left_eye_coor=center_coordinate[0]-int(size*0.3),center_coordinate[1]-int(size*0.2)
    mounth_center=center_coordinate[0],center_coordinate[1]+int(size*0.40)
    noise_center=center_coordinate[0],center_coordinate[1]+int(size*0.2)
    mounth_shape=int(size*0.3)
    right_ear_coor=center_coordinate[0]+int(size*0.3),center_coordinate[1]-int(size*0.6)
    left_ear_coor=center_coordinate[0]-int(size*0.4),center_coordinate[1]-int(size*0.6)
    cv2.ellipse(img,center_coordinate,(head_size,int(head_size*0.9)),0,0,360,color_head,cv2.FILLED)
    cv2.circle(img,right_eye_coor,eye_size,color_out,cv2.FILLED)
    cv2.circle(img,right_eye_coor,int(eye_size*0.8),color_inside,cv2.FILLED)
    cv2.circle(img,right_eye_coor,int(eye_size*0.3),color_out,cv2.FILLED)
    cv2.circle(img,left_eye_coor,eye_size,color_out,cv2.FILLED)
    cv2.circle(img,left_eye_coor,int(eye_size*0.8),color_inside,cv2.FILLED)
    cv2.circle(img,left_eye_coor,int(eye_size*0.3),color_out,cv2.FILLED)
    cv2.circle(img,noise_center,int(eye_size*0.8),color_out,cv2.FILLED)
    cv2.circle(img,noise_center,int(eye_size*0.3),color_inside,cv2.FILLED)
    cv2.line(img,noise_center,(noise_center[0]+int(head_size*0.3),noise_center[1]),color_out,2)
    cv2.line(img,noise_center,(noise_center[0]+int(head_size*0.3),noise_center[1]+int(head_size*0.1)),color_out,2)
    cv2.line(img,noise_center,(noise_center[0]-int(head_size*0.3),noise_center[1]),color_out,2)
    cv2.line(img,noise_center,(noise_center[0]-int(head_size*0.3),noise_center[1]+int(head_size*0.1)),color_out,2)
    cv2.circle(img,noise_center,int(eye_size*0.3),color_inside,cv2.FILLED)
    cv2.ellipse(img,mounth_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.6)),0,0,180,color_out,-1)
    cv2.ellipse(img,mounth_center,(change_month(mountion,mounth_shape),int(change_month(mountion,mounth_shape)*0.5)),0,0,180,eating(mountion,color_inside),-1)
    cv2.ellipse(img,right_ear_coor,(int(int(size*0.3)*1.9),int(size*0.2)),130,0,360,color_head,-1)
    cv2.ellipse(img,left_ear_coor,(int(int(size*0.3)*1.9),int(size*0.2)),50,0,360,color_head,-1)
    return img
