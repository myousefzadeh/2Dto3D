import cv2
import numpy as np
from matplotlib import pyplot as plt

imgC = cv2.imread('PlanSample1.jpg',0)
# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
#imgP = PIL.Image.open('PlanSample1.jpg').convert('RGB') 
#imgC = np.array(imgP) 
#imgP.show()
def LineSegment(Row,Cal, Prow,Pcal):
    MyW =[0 for tt in range(len(Prow))]
    for tt in range(len(Prow)):
        Inlier=[]
        allDists=[]
        print(Row,Cal,len(Prow))
        #print (Prow[0:10])
        #print (Pcal[0:10])
        if Pcal[tt]==Cal:
            Inlier = [elem for elem in range(tt) if Pcal[elem] == Cal ]
            SegPnt = [elem for elem in Inlier if elem ==Inlier[0] or Pcal[elem]-Pcal[elem-1]< 1]
            print (len(Inlier), len(SegPnt))
            print
        else:
            MyA = (Row-Prow[tt])/(Cal-Pcal[tt])
            Inlier = [elem for elem in range(tt) if abs(Prow[elem]-Row-MyA*(Pcal[elem]-Cal))<1]
            SegPnt = [elem for elem in Inlier if elem ==Inlier[0] or Prow[elem]-Row+(1/MyA)*(Pcal[elem]-Cal)-(Prow[elem-1]-Row+(1/MyA)*(Pcal[elem-1]-Cal))< 2]
            print (len(Inlier), len(SegPnt))
        MyW[tt] = len(allDists)
        if len(allDists)>0:
            print(Inlier)
    
    print('Line segment:', Row, Cal, 'to', Prow(MyW.index(max(MyW))),Pcal(MyW.index(max(MyW))),max(MyW))
    return Prow(MyW.index(max(MyW))),Pcal(MyW.index(max(MyW))),max(MyW), Inlier
#--- Main Program ---
edges = cv2.Canny(imgC,100,200)
points = np.asarray(np.where(edges == 255))
PointID = range(len(points[0]))
#print(len(points[0]))
W = imgC[0].size
H = int(imgC.size/imgC[0].size)
kernSize = 1
TanThr = .2
MyPatch= [[0 for x in range(kernSize*2+1)] for y in range(kernSize*2+1)]
#setattr(PixelAtt, 'foobar', 123)
CorMap = [[0 for x in range(W)] for y in range(H)]
LinMap = [[0 for x in range(W)] for y in range(H)]
LineData =[]
#LinMap[points[0][0]][points[1][0]] = LineLab
while PointID :
    k = PointID[0]
    ii = points[0][k]
    jj = points[1][k]
    IDsel=[]
    '''
    if edges[ii][jj-1]>0 :
        IDsel = [tt for tt in PointID if (points[0][tt]-ii)/(points[1][tt]-jj)<TanThr and (points[0][tt]-ii)/(points[1][tt]-jj)>-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    if edges[ii-1][jj-1]>0 :
        IDsel = [tt for tt in PointID if (points[0][tt]-ii)/(points[1][tt]-jj)<1+TanThr and (points[0][tt]-ii)/(points[1][tt]-jj)>1-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    if edges[ii-1][jj]>0 :
        IDsel = [tt for tt in PointID if (points[1][tt]-jj)/(points[0][tt]-ii)<TanThr and (points[1][tt]-jj)/(points[0][tt]-ii)>-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    if edges[ii-1][jj+1]>0 :
        IDsel = [tt for tt in PointID if (points[0][tt]-ii)/(points[1][tt]-jj)<-1+TanThr and (points[0][tt]-ii)/(points[1][tt]-jj)>-1-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    '''
    if edges[ii][jj+1]>0 :
        IDsel = [tt for tt in PointID if (points[0][tt]-ii)/(points[1][tt]-jj)<TanThr and (points[0][tt]-ii)/(points[1][tt]-jj)>-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    if edges[ii+1][jj+1]>0 :
        IDsel = [tt for tt in PointID if (points[0][tt]-ii)/(points[1][tt]-jj)<1+TanThr and (points[0][tt]-ii)/(points[1][tt]-jj)>1-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    if edges[ii+1][jj]>0 :
        IDsel = [tt for tt in PointID if (points[1][tt]-jj)/(points[0][tt]-ii)<TanThr and (points[1][tt]-jj)/(points[0][tt]-ii)>-TanThr]
        #print(points[0][IDsel[0]],points[1][IDsel[0]])
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
    if edges[ii+1][jj-1]>0 :
        IDsel = [tt for tt in PointID if (points[1][tt]-jj)/(points[0][tt]-ii)<-1+TanThr and (points[1][tt]-jj)/(points[0][tt]-ii)>-1-TanThr]
        Ei,Ej,MyMax, MyInlier = LineSegment(ii,jj, points[0][IDsel],points[1][IDsel])
        PointID = list(set(PointID)-set(MyInlier))
        LineData.append([ii,jj,Ei,Ej,MyMax])
'''   

#print(imgC[ii-edges+tti][jj-kernSize:jj+kernSize])#,imgC[ii-2+tti][jj-1],imgC[ii-2+tti][jj],imgC[ii-2+tti][jj+1],imgC[ii-2+tti][jj+2])
            
CCCC = np.divide(CorMap,LineLab)          
plt.subplot(121),plt.imshow(imgC,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.scatter(points[1],points[0],)
#plt.subplot(122),plt.imshow(edges,cmap = 'YlGn')
plt.subplot(122),plt.imshow(LinMap,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()


edgesP = PIL.Image.fromarray(edges)

pixelsIM = imgP.load() # create the pixel map for original image
pixelsED = edgesP.load() # create the pixel map for edge Image
print('Original image size:',imgP.size[0],imgP.size[0],'Edge image size:',edgesP.size[0],edgesP.size[0])



for i in range(imgP.size[0]):    # for every col:
    for j in range(imgP.size[1]):    # For every row
        if pixelsED[i,j]>0

        pixels[i,j] = (i, j, 100) # set the colour accordingly
        


'''
