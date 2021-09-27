import cv2
from .SimpleHRNet import SimpleHRNet
import time
import os

font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (50, 50)
  
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (255, 0, 0)
  
# Line thickness of 2 px
thickness = 2

# function that takes as input the path of image and returns the joints by running inference on the hrnet model
def get_joints(path):
    # load the model
    model = SimpleHRNet(32, 17, "pose_hrnet_w32_256x192.pth", resolution=(256, 192), multiperson=False)

    # load the image
    image = cv2.imread(os.path.join("./media", path))
    print(path)
    start = time.time()
    joints = model.predict(image)
    end = time.time()
    print("Time taken for inference: ", end - start)
    points = []
    for i, coords in enumerate(joints[0]):
            y, x, _ = coords
            points.append([x,y])
            image = cv2.circle(image, (x,y), radius=3, color=(0, 0, 255), thickness=-1)
            image = cv2.putText(image, str(i), (x,y), font, 
                        fontScale, color, thickness, cv2.LINE_AA)

    cv2.imwrite(os.path.join("./media", "output.jpg"), image)

    return points

#function to return distance between two points given as a list
def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# function to get measurements by upscaling points with height
def get_measurements(points, height):
    leftShoulder = points[6]
    rightShoulder = points[5]
    leftFoot = points[16]
    rightFoot = points[15]
    leftElbow = points[8]
    rightElbow = points[7]
    leftWaist = points[12]
    rightWaist = points[11]

    #calculate pixel height by taking distance between foot and shoulder of both sides and taking average
    pixelHeight = (distance(leftShoulder, leftFoot) + distance(leftElbow, leftShoulder)
                    + distance(rightElbow, rightShoulder) + distance(rightShoulder, rightFoot))/2

    # calculate the distance between the left and right shoulders
    shoulderDistance = distance(leftShoulder, rightShoulder)
    
    # calculate waist
    waistDistance = distance(leftWaist, rightWaist)

    # calculate length of torso by taking average of distances between left elbow left waist right elbow right waist
    torso = (distance(leftShoulder, leftWaist) + distance(rightShoulder, rightWaist)) / 2

    # caluclate distance of lower body by taking similar average as torso
    lower = (distance(leftWaist, leftFoot) + distance(rightWaist, rightFoot)) / 2

    # upscale all distances by taking height as refernce and downscale using pixelHeight
    shoulderDistance = shoulderDistance * height / pixelHeight
    waistDistance = waistDistance * height * 3 / pixelHeight
    torso = torso * height / pixelHeight
    lower = lower * height * 1.1 / pixelHeight

    # return all distances
    return int(shoulderDistance), int(waistDistance), int(torso), int(lower)

