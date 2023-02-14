"""
Show image
Three point circle
Calculate number of pixels in the circle
Save info

"""

# importing the module
import cv2
import numpy as np
import time
import os


def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    
    if abs(det) < 1.0e-6:
        return (None, np.inf)
    
    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return ((int(cx), int(cy)), int(radius))



# function to display the coordinates of
# of the points clicked on the image 

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN: # Save left click coordinates
        print(x, ' ', y)
        circlePoints.append((x,y))

    # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN: # Exit at right click
        print("CP ", circlePoints)
        time.sleep(0.2)
        cv2.destroyAllWindows()


  



#img = cv2.imread(r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\tempCandida\train\A35.3.jpg", 1)
path = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\petripixels/"
images = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg")]

amount = len(images)

outputName = os.path.join(path, "petriPixels.txt")

# with open(os.path.join(outputName), 'w') as f:
#     f.write(f'image,petriPixels\n')


for i in images:
    circlePoints = []

    base = os.path.basename(i)
    imageName = os.path.splitext(base)[0]


    img = cv2.imread(i,1)

    # Create a window for the image (avoiding images not fitting the screen)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("image", 350, 100)
    cv2.resizeWindow("image", 800, 600)

    cv2.imshow("image", img)

    cv2.setMouseCallback('image', click_event) # setting mouse handler for the image and calling the click_event() function

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    ### Circle stuff
    c = define_circle(circlePoints[0], circlePoints[1], circlePoints[2])

    white = np.ones_like(img)
    mask = cv2.circle(white, c[0], c[1], (255,255,255), -1)

    # # put mask into alpha channel of input
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask[:,:,0]

    #resultBlack = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    #resultBlack[:, :, 3] = mask[:,:,0]

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    gray[:, :,] = mask[:,:,0]
    nzCount = cv2.countNonZero(gray)
    cv2.imwrite(os.path.join(path, "petriCrops", imageName + "_petri.png"), result)
    cv2.imwrite(os.path.join(path, "petriCrops", imageName + "_mask.png"), gray)
    print(nzCount)

    n_white_pix = np.sum(gray == 255)
    print('Number of white pixels:', n_white_pix)

    with open(os.path.join(outputName), 'a') as f:
        f.write(f'{imageName},{n_white_pix}\n')

    amount -= 1
    print("Files left: ", amount)