import cv2
import numpy as np
from matplotlib import pyplot as plt

imgC = cv2.imread('PlanSample1.jpg',0)
# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
#imgP = PIL.Image.open('PlanSample1.jpg').convert('RGB') 
#imgC = np.array(imgP) 
#imgP.show()

edges = cv2.Canny(imgC,100,200)
points = np.asarray(np.where(edges == 255))
print(len(points))


plt.subplot(121),plt.imshow(imgC,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.scatter(points[1],points[0])
plt.show()
'''
edgesP = PIL.Image.fromarray(edges)

pixelsIM = imgP.load() # create the pixel map for original image
pixelsED = edgesP.load() # create the pixel map for edge Image
print('Original image size:',imgP.size[0],imgP.size[0],'Edge image size:',edgesP.size[0],edgesP.size[0])



for i in range(imgP.size[0]):    # for every col:
    for j in range(imgP.size[1]):    # For every row
        if pixelsED[i,j]>0

        pixels[i,j] = (i, j, 100) # set the colour accordingly
        
'''



