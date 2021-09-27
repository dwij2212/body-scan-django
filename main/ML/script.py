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

    return joints[0]
