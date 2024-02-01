# %%
#OpenCV + Python script for inspecting (counting) pills during manufacturing

import cv2
import numpy as np
# import imutils
import matplotlib.pyplot as plt
#%matplotlib inline
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 




# %%
def NumberOfPills():
    cam_port = 0
    url = 'http://10.1.133.124:8080/video'

    cam = cv2.VideoCapture(url) 
    
    # reading the input using the camera 
    result, image = cam.read() 
    
    # If image will detected without any error,  
    # show result 
    if result: 
    
        # showing result, it take frame name and image  
        # output 
        # cv2.imshow("Preet", image)
    
        # saving image in local storage 
        cv2.imwrite("Preet.png", image) 
    
        # If keyboard interrupt occurs, destroy image  
        # window 
        cv2.waitKey(0)
        cam.release()
        # cv2.destroyWindow("Preet") 
    
    # If captured image is corrupted, moving to else part
    else: 
        print("No image detected. Please! try again") 

    # %%
    # Read an image
    img = cv2.imread('Preet.png') 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    # %%
    # plt.imshow(img)

    # %%
    # Convert the image in a numpy array

    img = np.array(img, dtype=np.uint8)

    # %%
    fx = fy = int(200.0 / img.shape[0])

    # %%
    dim = (100, int(img.shape[1] * fx))

    # %%
    # Resize the original image

    resized = cv2.resize(img, dim, fx = 0.5,fy=0.5)

    # %%
    # Apply Gaussian blur 
    blur = cv2.GaussianBlur(resized,(7,7),0)

    # %%
    roi_hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)

    # %%
    # plt.imshow(roi_hsv)

    # %%
    # Convert the image in HSV 

    h, s, v = cv2.split(roi_hsv)
    hsv_image = cv2.merge([h, s, v])

    # %%
    # plt.imshow(s)

    # %%
    imgOTSU = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # %%
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5),(1,1))

    # %%
    # plt.imshow(imgOTSU[1])

    # %%
    fgmask = cv2.morphologyEx(imgOTSU[1], cv2.MORPH_CLOSE, kernel)

    # %%
    # plt.imshow(fgmask)

    # %%
    PillsContours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  


    # %%
    # filtered_contours = [contour for contour in PillsContours if cv2.contourArea(contour) > 2000]
    filtered_contours = [contour for contour in PillsContours if cv2.contourArea(contour) > 1000 and cv2.contourArea(contour) < 6000]

    # Draw the filtered contours on a blank image (optional)
    # result_image = cv2.drawContours(np.zeros_like(fgmask), filtered_contours, -1, (255, 255, 255), thickness=cv2.FILLED)
    # result_image

    # %%
    # print ('Number of pills: ', len(PillsContours))
    print ('Number of pills: ', len(filtered_contours))
    processed_image = cv2.drawContours(np.zeros_like(fgmask), filtered_contours, -1, (255, 255, 255), thickness=cv2.FILLED)
    return len(filtered_contours),img,processed_image
