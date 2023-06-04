import streamlit as st
import requests
from matplotlib import pyplot as plt
import cv2
import numpy as np
from PIL import Image
st.set_page_config(page_title="PCB Detection",page_icon=":tada:",layout="wide")

st.title("PCB Detection")
import requests

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image. Status code:", response.status_code)


image_url = "http://127.0.0.1:8800/image"
save_file_path = "input.jpg"
download_image(image_url, save_file_path)

def imshow(title = "", image = None, size = 10):
    w, h = image.shape[0], image.shape[1]
    aspectRatio = w / h
    plt.figure(figsize=(size * aspectRatio, size))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

def getContours(imageFile):
    grayScaleImage2 = cv2.cvtColor(imageFile, cv2.COLOR_BGR2GRAY)
    edgedImage = cv2.Canny(grayScaleImage2, 30, 200)

    contours, hierarchy = cv2.findContours(edgedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def difference(val1, val2):
    setContours1 = set(map(tuple, [np.ravel(contour).tolist() for contour in val1]))
    setContours2 = set(map(tuple, [np.ravel(contour).tolist() for contour in val2]))

    diffContours = setContours1 - setContours2

    numDiffContours = len(diffContours)
    return numDiffContours

sourceImage = cv2.imread('standard.jpg')
imshow('Source Image', sourceImage, 5)
print('Source Image RES: ', sourceImage.shape[0],'x',sourceImage.shape[1])


st.image(sourceImage,width=500, caption='source Image')

inputImage = cv2.imread('input.jpg')
imshow('Input Image', inputImage, 5)
print('Input Image RES: ', inputImage.shape[0],'x',inputImage.shape[1])

st.image(inputImage,width=500, caption='Input Image')
difference(getContours(sourceImage), getContours(inputImage))

height, width, channels = sourceImage.shape

quadrant_width = width // 2
quadrant_height = height // 2

sQ1 = sourceImage[:quadrant_height, :quadrant_width, :]
sQ2 = sourceImage[:quadrant_height, quadrant_width:, :]
sQ3 = sourceImage[quadrant_height:, :quadrant_width, :]
sQ4 = sourceImage[quadrant_height:, quadrant_width:, :]


height, width, channels = inputImage.shape

quadrant_width = width // 2
quadrant_height = height // 2

iQ1 = inputImage[:quadrant_height, :quadrant_width, :]
iQ2 = inputImage[:quadrant_height, quadrant_width:, :]
iQ3 = inputImage[quadrant_height:, :quadrant_width, :]
iQ4 = inputImage[quadrant_height:, quadrant_width:, :]

sourceImageArray = [sQ1, sQ2, sQ3, sQ4]
inputImageArray = [iQ1, iQ2, iQ3, iQ4]

effectedAreaList = []
for i in range(len(sourceImageArray)):
    diff = difference(getContours(sourceImageArray[i]), getContours(inputImageArray[i]))
    if diff != 0:
        effectedAreaList.append(1)
    else:
        effectedAreaList.append(0) 

Quadrant1=[1,0,0,0]
Quadrant2=[0,1,0,0]
Quadrant3=[0,0,1,0]
Quadrant4=[0,0,0,1]
if effectedAreaList==Quadrant1:
    st.subheader("Defect detected in Quadrant 1")
    st.image(iQ1,width=500, caption='Input Quadrant 1')
elif effectedAreaList==Quadrant2:
    st.subheader("Defect detected in Quadrant 2")
    st.image(iQ2,width=500, caption='Input Quadrant 2')
elif effectedAreaList==Quadrant3:
    st.subheader("Defect detected in Quadrant 3")
    st.image(iQ3,width=500, caption='Input Quadrant 3')
elif effectedAreaList==Quadrant4:
    st.subheader("Defect detected in Quadrant 4")
    st.image(iQ4,width=500, caption='Input Quadrant 4')
else:
    st.write("PCB is not Defected")