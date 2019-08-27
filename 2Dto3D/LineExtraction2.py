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

#print(len(points[0]))
W = imgC[0].size
H = int(imgC.size/imgC[0].size)
kernSize = 1
MyPatch= [[0 for x in range(kernSize*2+1)] for y in range(kernSize*2+1)]
#setattr(PixelAtt, 'foobar', 123)
CorMap = [[0 for x in range(W)] for y in range(H)]
LinMap = [[0 for x in range(W)] for y in range(H)]

#LinMap[points[0][0]][points[1][0]] = LineLab
for k in range(len(points[0])):
    
    MyW=[0 for x in range(len(points[0]))]
    ii = points[0][k]
    jj = points[1][k]
    print('Point:',k, 'Coordinate:',ii,jj)
    for tt in range(k+1,len(points[0])):
        Inlier=[]
        allDists=[]
        if points[0][tt]==ii:
            Inlier = [elem for elem in range(k+1,tt+1) if points[0][elem] == ii ]
            #print(points[0][Inlier])
            allDists = [points[1][elem] for elem in Inlier if elem==Inlier[0] or points[1][elem]-points[1][elem-1]< 2]
        else:
            MyA = (ii-points[0][tt])/(jj-points[1][tt])
            Inlier = [elem for elem in range(k+1,tt+1) if abs(points[0][elem]-ii-MyA*(points[1][elem]-jj)) < 1 ]
            allDists = [points[0][elem]-ii+(1/MyA)*(points[1][elem]-jj) for elem in Inlier if elem==Inlier[0] or points[0][elem]-ii+(1/MyA)*(points[1][elem]-jj)-(points[0][elem-1]-ii+(1/MyA)*(points[1][elem-1]-jj))< 2]
        if not allDists or allDists[0]<2:
            MyW[tt] = len(allDists)
        if tt%100==0:
            print('here:', tt)
        
    if max(MyW)>10:
        print(MyW.index(max(MyW)))
    
    #print(max(MyW))

    #while EE2-EE1 < DistTol and 
#print(imgC[ii-edges+tti][jj-kernSize:jj+kernSize])#,imgC[ii-2+tti][jj-1],imgC[ii-2+tti][jj],imgC[ii-2+tti][jj+1],imgC[ii-2+tti][jj+2])
            
CCCC = np.divide(CorMap,LineLab)          
plt.subplot(121),plt.imshow(imgC,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.scatter(points[1],points[0],)
#plt.subplot(122),plt.imshow(edges,cmap = 'YlGn')
plt.subplot(122),plt.imshow(LinMap,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
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
