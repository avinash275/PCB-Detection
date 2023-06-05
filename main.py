import streamlit as st
import requests
from matplotlib import pyplot as plt
import cv2
import numpy as np
from PIL import Image
import os
import tempfile
st.set_page_config(page_title="PCB Detection",page_icon=":tada:",layout="wide")
st.title("PCB Detection")
import requests

#for taking image from api
# def download_image(url, save_path):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(save_path, 'wb') as file:
#             file.write(response.content)
#         print("Image downloaded successfully.")
#     else:
#         print("Failed to download image. Status code:", response.status_code)
# image_url = "http://127.0.0.1:8800/image"
# save_file_path = "input.jpg"
# download_image(image_url, save_file_path)

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
st.subheader("PCB Image Uploader")

inputImage = st.file_uploader("Choose PCB Image...", type=["jpg", "jpeg"])
if inputImage is not None:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(inputImage.read())
    temp_file.close()
    image_path = temp_file.name
    xinputi= cv2.imread(image_path)
    with st.container():
        st.write("---")
        source_column,output_column=st.columns(2)
        with source_column:
            st.image(sourceImage,width=500, caption='source Image')
        with output_column:
            st.image(inputImage,width=500, caption='Input Image')
    difference(getContours(sourceImage), getContours(xinputi))
    height, width, channels = sourceImage.shape

    quadrant_width = width // 2
    quadrant_height = height // 2

    sQ1 = sourceImage[:quadrant_height, :quadrant_width, :]
    sQ2 = sourceImage[:quadrant_height, quadrant_width:, :]
    sQ3 = sourceImage[quadrant_height:, :quadrant_width, :]
    sQ4 = sourceImage[quadrant_height:, quadrant_width:, :]


    height, width, channels = xinputi.shape

    quadrant_width = width // 2
    quadrant_height = height // 2

    iQ1 = xinputi[:quadrant_height, :quadrant_width, :]
    iQ2 = xinputi[:quadrant_height, quadrant_width:, :]
    iQ3 = xinputi[quadrant_height:, :quadrant_width, :]
    iQ4 = xinputi[quadrant_height:, quadrant_width:, :]

    sourceImageArray = [sQ1, sQ2, sQ3, sQ4]
    inputImageArray = [iQ1, iQ2, iQ3, iQ4]
    st.write("---")
    effectedAreaList = []
    for i in range(len(sourceImageArray)):
        diff = difference(getContours(sourceImageArray[i]), getContours(inputImageArray[i]))
        if diff != 0:
            effectedAreaList.append(1)
        else:
            effectedAreaList.append(0) 
    if effectedAreaList==[0,0,0,0]:
        st.subheader("PCB is not Defected")
    else:
        for i in range(0,len(effectedAreaList)):
            if i==0:
                iQ=iQ1
                sQ=sQ1
            elif i==1:
                iQ=iQ2
                sQ=sQ2
            elif i==2:
                iQ=iQ3
                sQ=sQ3
            else:
                iQ=iQ4
                sQ=sQ4
            if effectedAreaList[i]==1:
                st.subheader(f"Defect detected in Quadrant {i+1}")
                with st.container():
                    st.write("---")
                    source_column,output_column=st.columns(2)
                    with source_column:
                        st.image(sQ,width=500, caption=f'Source Quadrant {i+1}')
                    with output_column:
                        st.image(iQ,width=500, caption=f'Input Quadrant {i+1}')
