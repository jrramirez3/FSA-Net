import numpy as np
import math
import os
import re
from PIL import Image

def getFMatrix(roll, pitch, yaw):
    SR = math.sin(math.radians(roll))
    SP = math.sin(math.radians(pitch))
    SY = math.sin(math.radians(yaw))
    CR = math.cos(math.radians(roll))
    CP = math.cos(math.radians(pitch))
    CY = math.cos(math.radians(yaw))
    M = np.zeros((3,3))
    M[0][0]=CP*CY
    M[0][1]=CP*SY
    M[0][2]=SP
    M[1][0]=SR*SP*CY-CR*SY
    M[1][1]=SR*SP*SY+CR*CY
    M[1][2]=-SR*CP
    M[2][0]=-(CR*SP*CY+SR*SY)
    M[2][1]=(CY*SR)-(CR*SP*SY)
    M[2][2]=CR*CP
    return M

def preprocessquats():
    for root, dirs, files in os.walk("C:\\Users\\marky\\Documents\\GazeEstimationProjects\\FSA-Net\\GazeDatasets"):
        for file in files:
            if file.endswith(".txt"):
                fulltextfilename = os.path.join(root, file)
                # print(fulltextfilename)
                myfile = open(fulltextfilename, "rt") # open lorem.txt for reading text
                contents = myfile.read()         # read the entire file into a string
                myfile.close()                   # close the file
                # print(contents)                  # print contents
                text = contents
                pitch = re.search('P=(.+?) Y=', text).group(1)
                yaw = re.search('Y=(.+?) R=', text).group(1)
                roll = re.search('R=(.+?);X=', text).group(1)
                xpos = re.search('X=(.+?) Y=', text).group(1)
                ypostxt = text[text.rfind('Y'):len(text)]
                ypos = re.search('Y=(.+?) Z=', ypostxt).group(1)
                zpos = text.split("Z=",1)[1]
                M = getFMatrix(float(roll), float(pitch), -float(yaw))
                # m = re.search('Z=(.+?)', text) # Search between substrings
                # m2 = text.split("Z=",1)[1] # Search string after substring
                # print(m2)
                # if m:
                #     found = m.group(1)
                    # print(found)
                print("str(xpos): " + str(xpos))
                print("str(ypos): " + str(ypos))
                print("str(zpos): " + str(zpos))
                finalTxtStr = str(M[0][0]) + " " + str(M[0][1]) + " " + str(M[0][2]) + " \n" + str(M[1][0]) + " " + str(M[1][1]) + " " + str(M[1][2]) + " \n" + str(M[2][0]) + " " + str(M[2][1]) + " " + str(M[2][2]) + " \n\n" + str(xpos) + " " + str(ypos) + " " + str(zpos)
                fullfilepath = fulltextfilename[0:fulltextfilename.rfind('\\')] + "\\"
                filenumname = fulltextfilename[fulltextfilename.rindex('\\')+1:][:-4]
                newfilename = filenumname + "final"
                fullnewfilename = fullfilepath + newfilename + ".txt"
                text_file = open(fullnewfilename, "w")
                text_file.write(finalTxtStr)
                text_file.close()

def cropImageAtCenter(imgdir, new_width, new_height):
    # preprocessrgbs()
    # im = Image.open("C:\\Users\\marky\\Documents\\GazeEstimationProjects\\FSA-Net\\GazeDatasets\\MaleBlack1\\cam1\\1.png")
    im = Image.open(imgdir)
    width, height = im.size   # Get dimensions

    # new_width = 640
    # new_height = 480
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    return im
    # im.save("C:\\Users\\marky\\Documents\\GazeEstimationProjects\\FSA-Net\\GazeDatasets\\MaleBlack1\\cam1\\1-out.png")

def preprocessrgbs():
    for root, dirs, files in os.walk("C:\\Users\\marky\\Documents\\GazeEstimationProjects\\FSA-Net\\GazeDatasets"):
        for file in files:
            if file.endswith(".png"):
                fullimgfilename = os.path.join(root, file)
                fullfilepath = fullimgfilename[0:fullimgfilename.rfind('\\')] + "\\"
                filenumname = fullimgfilename[fullimgfilename.rindex('\\')+1:][:-4]
                newfilename = filenumname + "final"
                fullnewfilename = fullfilepath + newfilename + ".png"

                im = cropImageAtCenter(fullimgfilename, 640, 480)
                im.save(fullnewfilename)
                print(fullnewfilename)

if __name__ == "__main__":
    preprocessrgbs()
