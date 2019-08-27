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
LineLab=1
LinMap[points[0][0]][points[1][0]] = LineLab
for k in range(len(points[0])):
    ii = points[0][k]
    jj = points[1][k]
    #edges[ii][jj]
    if ii-kernSize>0 and ii+kernSize<H and jj-kernSize>0 and jj+kernSize<W:
        '''
        print('Sample:',ii,jj)
        for tti in range(kernSize*2+1):
            for ttj in range(kernSize*2+1):
                MyPatch[tti][ttj]=edges[ii-kernSize+tti][jj-kernSize+ttj]
                            
            print(MyPatch[tti])
        '''
        if edges[ii][jj-1]>0 and ( edges[ii][jj+1]>0 or edges[ii+1][jj+1]>0 or edges[ii-1][jj+1]>0):
            if LinMap[ii][jj-1]>0:
                LinMap[ii][jj] = LinMap[ii][jj-1]
            else:
                LinMap[ii][jj] = LineLab
            
        elif edges[ii-1][jj-1]>0 and ( edges[ii+1][jj+1]>0 or edges[ii][jj+1]>0 or edges[ii+1][jj]>0):
            if LinMap[ii-1][jj-1]>0:
                LinMap[ii][jj] = LinMap[ii-1][jj-1]
            else:
                LinMap[ii][jj] = LineLab
        elif edges[ii-1][jj]>0 and ( edges[ii+1][jj]>0 or edges[ii+1][jj-1]>0 or edges[ii+1][jj+1]>0):
            if LinMap[ii-1][jj]>0:
                LinMap[ii][jj] = LinMap[ii-1][jj]>0
            else:
                LinMap[ii][jj] = LineLab
        elif edges[ii-1][jj+1]>0 and ( edges[ii+1][jj-1]>0 or edges[ii][jj-1]>0 or edges[ii+1][jj]>0):
            if LinMap[ii-1][jj+1]:
                LinMap[ii][jj] = LinMap[ii-1][jj+1]>0
            else:
                LinMap[ii][jj] = LineLab
        else:
            print('Sample:',ii,jj)
            CorMap[ii][jj] = 1
            LineLab += 1
        
print('Cornerpoint Num:',LineLab) 
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
