from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import main
import cv2
import os

# Window config
root = tk.Tk()
root.geometry("1100x600")
root.resizable(False,False)
root.title("Face Recognition App")

# Typography
font = ('inter', 18, 'bold')
rgFont = ('inter', 10)
frameStyle = ttk.Style()
frameStyle.configure('body.TFrame', background="#F9FDF9")
colorPallete = "#F8F9F8"
# Title Section
# Title Frame
titleFrame = ttk.Frame(root, width=100, height=50, style='body.TFrame', border=1)
titleFrame.pack(fill="both", expand=1)
# Title Contents
titleContent = ttk.Label(titleFrame, text="Face Recognition",font=('Inter 25 bold'), background=colorPallete)
titleContent.place(relx=0.5, rely=0.5, anchor=CENTER)

# Body Section
# Body Frame
bodyFrame = ttk.Frame(root, width=100, style='body.TFrame')
bodyFrame.pack(fill="both", expand=1)

# LHS Section
# Choose dataset label & button
btnImg1 = "./assets/datasetBtn.png"
datasetBtn = Image.open(btnImg1)
datasetBtn = datasetBtn.resize((152, 36))
datasetBtn = ImageTk.PhotoImage(datasetBtn)
chooseDatasetLabel = tk.Label(bodyFrame, text='Choose a dataset folder', width=25, font = font, background=colorPallete)
chooseDatasetLabel.grid(row=1,column=0, pady=10)
chooseDatasetBtn = tk.Button(bodyFrame, command = lambda:uploadDatasetFile(), width=170, height=36, image=datasetBtn, borderwidth=0, background=colorPallete)
chooseDatasetBtn.grid(row=2, column=0)
datasetStatusLabel = tk.Label(bodyFrame, text='No File Choosen', width=25, font = rgFont, background=colorPallete)
datasetStatusLabel.grid(row=3, column=0)

# Choose test image label & button
# Choose dataset label & button
btnImg2 = "./assets/testImgBtn.png"
testImgBtn = Image.open(btnImg2)
testImgBtn = testImgBtn.resize((152, 36))
testImgBtn = ImageTk.PhotoImage(testImgBtn)
chooseTestImgLabel = tk.Label(bodyFrame, text='Choose a test image', width=25, font= font, background=colorPallete)
chooseTestImgLabel.grid(row=4,column=0, pady=10)
chooseImgTestBtn = tk.Button(bodyFrame, command = lambda:uploadTestFile(), image=testImgBtn, width=170, height=36, borderwidth=0, background=colorPallete)
chooseImgTestBtn.grid(row=5, column=0)
testFaceStatusLabel = tk.Label(bodyFrame, text='No File Choosen', width=60, font = rgFont, background=colorPallete)
testFaceStatusLabel.grid(row=6, column=0)

# Run Button
btnImg3 = "./assets/startBtn.png"
runImgBtn = Image.open(btnImg3)
runImgBtn = runImgBtn.resize((152, 36))
runImgBtn = ImageTk.PhotoImage(runImgBtn)
runBtn = tk.Button(bodyFrame, command = lambda:startRecognize(), image=runImgBtn, width=170, height=36, borderwidth=0, pady=10, background=colorPallete)
runBtn.grid(row = 15, column=1, columnspan=2, pady=20)

# RHS Section
# Test Image Section
# Test Image Label
testImgLabel = tk.Label(bodyFrame, text='Test Image', width=30, background=colorPallete)
testImgLabel.grid(row=1, column=1)
# Test Image Container & Image
imagePath = "./assets/baseImage.jfif"
originalImage = Image.open(imagePath)
resizedImage = originalImage.resize((256,256))
testImg = ImageTk.PhotoImage(resizedImage)
testImgContainer1 = tk.Button(bodyFrame, image=testImg, borderwidth=0)
testImgContainer1.grid(row=2, column=1, rowspan=5, padx=10)

# Result Image Label
resultImgLabel = tk.Label(bodyFrame, text='Closest Image', width=30, background=colorPallete)
resultImgLabel.grid(row=1, column=2)
# Result Image Container & Image
testImgContainer2 = tk.Button(bodyFrame, image=testImg, borderwidth=0)
testImgContainer2.grid(row=2, column=2, rowspan=5)

# Callbacks
def uploadDatasetFile():
    global datasetDirectory
    datasetDirectory = filedialog.askdirectory()
    datasetDirectoryStr = datasetDirectory
    datasetDirectoryStr = os.path.basename(datasetDirectoryStr)
    datasetStatusLabel = tk.Label(bodyFrame, text = datasetDirectoryStr, width=60, font = rgFont, background=colorPallete)
    datasetStatusLabel.grid(row=3, column=0)

def uploadTestFile():
    global sampleDirectory, imgTest, testFaceStatusLabel
    sampleDirectory = filedialog.askopenfilename()
    fetchedImg = Image.open(sampleDirectory)
    resizeImg = fetchedImg.resize((256,256))
    imgTest = ImageTk.PhotoImage(resizeImg)
    testImgReplace = tk.Button(bodyFrame, image = imgTest, borderwidth=0)
    testImgReplace.grid(row=2, column=1, rowspan=5, padx=10)
    sampleDirectoryStr = os.path.basename(sampleDirectory)
    testFaceStatusLabel = tk.Label(bodyFrame, text = sampleDirectoryStr, width=60, font = rgFont, background=colorPallete)
    testFaceStatusLabel.grid(row=6, column=0)

def closeCam():
    global endCam, frame, countImage, camera
    endCam = True
    if (endCam):
        imageName = "../bin/sample_image_" + str(countImage) + ".jpg"
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        cv2.imwrite(imageName, frame)
        countImage += 1
        successMsg = tk.Label(bodyFrame, text="Closed camera! Please select the test face image!", width=40, background=colorPallete)
        successMsg.grid(row = 11, column=1, columnspan=10)
        camera.release()
        cv2.destroyAllWindows()
        runBtn.grid(row = 9, column=1, columnspan=2)

def startRecognize():
    global resultImage, currTime, startTime
    startTime = time.time()
    finalResultPath, matchPercentage = main.run(datasetDirectory, sampleDirectory)
    currTime = round(time.time() - startTime, 3)
    executionTimeLabel = tk.Label(bodyFrame, text="Execution Time: " + str(currTime) + " seconds", background=colorPallete)
    executionTimeLabel.grid(row=8, column=0)
    filename = finalResultPath
    fetchedImg = Image.open(filename)
    resizeImg = fetchedImg.resize((256,256))
    resultImage = ImageTk.PhotoImage(resizeImg)
    resultReplace = tk.Button(bodyFrame, image = resultImage, borderwidth=0)
    resultReplace.grid(row=2, column=2, rowspan=5, padx=10)
    filenameStr = os.path.basename(filename)
    testFaceStatusLabel = tk.Label(bodyFrame, text = filenameStr, width=60, font = rgFont, background=colorPallete)
    testFaceStatusLabel.grid(row=6, column=0)
root.mainloop()