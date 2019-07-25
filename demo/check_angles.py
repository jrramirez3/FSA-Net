import os
import cv2
import sys
import numpy as np
from math import cos, sin
# from demo_FSANET_mtcnn import *

def draw_axis(img, yaw, pitch, roll, tdx=None, tdy=None, size = 80):
    
    # pitch = pitch * np.pi / 180
    # yaw = -(yaw * np.pi / 180)
    # roll = roll * np.pi / 180

    print(pitch, yaw, roll)

    if tdx != None and tdy != None:
        tdx = tdx
        tdy = tdy
    else:
        height, width = img.shape[:2]
        tdx = width / 2
        tdy = height / 2

    # X-Axis pointing to right. drawn in red
    x1 = size * (cos(yaw) * cos(roll)) + tdx
    y1 = size * (cos(pitch) * sin(roll) + cos(roll) * sin(pitch) * sin(yaw)) + tdy

    # Y-Axis | drawn in green
    #        v
    x2 = size * (-cos(yaw) * sin(roll)) + tdx
    y2 = size * (cos(pitch) * cos(roll) - sin(pitch) * sin(yaw) * sin(roll)) + tdy

    # Z-Axis (out of the screen) drawn in blue
    x3 = size * (sin(yaw)) + tdx
    y3 = size * (-cos(yaw) * sin(pitch)) + tdy

    cv2.line(img, (int(tdx), int(tdy)), (int(x1),int(y1)),(0,0,255),3)
    cv2.line(img, (int(tdx), int(tdy)), (int(x2),int(y2)),(0,255,0),3)
    cv2.line(img, (int(tdx), int(tdy)), (int(x3),int(y3)),(255,0,0),2)

    # cv2.imshow('image with lines',img)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()

    return img
    

def main():
    img_size = 64

    faces = np.empty((img_size, img_size, 4))

    src = '../testdata/'
    num =  1
    img = '1skbx1'
    bbox = '1-bbox'

    img_path = src + img + '.png'
    txt_path = src + str(num) + '.txt'
    bbox_path = src + bbox + '.txt'

    # print(orig_img)
    original = cv2.imread(img_path, -1)
    img_height, img_width, channels=original.shape
    print(img_height, img_width, channels)
    cv2.imshow('original', original)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

    file = open(txt_path,'r')
    for line in file:
        coords = line.split(';')
    # print(coords)
    rots = coords[0].split(' ')
    pose = coords[1].split(' ')
    rotations=[]
    poses=[]

    for x in range(0,3):
        rotations.append((rots[x].split('=')[1]))
        poses.append((pose[x].split('=')[1]))

    print(rotations)

    pitch = float(rotations[0])
    yaw = float(rotations[1])
    roll = float(rotations[2])

    x = int(float(poses[0]))
    y = int(float(poses[1]))
    z = float(poses[2])

    print(poses)

    bbox_file = open(bbox_path, 'r')
    for line in bbox_file:
        bbox_coords = line.split(' ')

    print(bbox_coords)
    xmin = int(bbox_coords[0])
    ymin = int(bbox_coords[1])
    xmax = int(bbox_coords[2])
    ymax = int(bbox_coords[3])
    print(xmin, ymin, xmax, ymax)
    rectangle=cv2.rectangle(original,(xmin, ymin), (xmax, ymax),(0,0,255),1)
    cv2.imshow('with bounding box', rectangle)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

    # image=draw_axis(original,yaw,pitch,roll,tdx=None, tdy=None, size=80)

    faces[:,:,:] = cv2.resize(original[ymin:ymax + 1, xmin:xmax + 1, :], (img_size, img_size))
    faces[:,:,:] = cv2.normalize(faces[:,:,:], None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)        

    img = draw_axis(original[ymin:ymax + 1, xmin:xmax + 1, :], yaw, pitch, roll)       

    original[ymin:ymax + 1, xmin:xmax + 1, :] = img
                
    cv2.imshow("result", original)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

    # cv2.imwrite('original',original)
    # circle=cv2.circle(original,(x,y),64,(0,0,255),-1)
    # cv2.imshow('original', circle)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()
    
    # draw_axis(img, yaw, pitch, roll, tdx=None, tdy=None, size = 80):

    

if __name__ == '__main__':
    main()