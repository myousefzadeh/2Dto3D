import cv2
import numpy as np
from matplotlib import pyplot as plt

imgC = cv2.imread('PlanSample1.jpg',0)
# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
#imgP = PIL.Image.open('PlanSample1.jpg').convert('RGB') 
#imgC = np.array(imgP) 
#imgP.show()

#--- Main Program ---
edges = cv2.Canny(imgC,100,200)
W = len(edges[0])
H = len(edges)
kernSize = 2
MyPatch= [[0 for x in range(kernSize*2+1)] for y in range(kernSize*2+1)]
#setattr(PixelAtt, 'foobar', 123)
#CorMap = [[0 for x in range(W)] for y in range(H)]
#LinMap = [[0 for x in range(W)] for y in range(H)]
LineData =[]
TestIm = edges>0
TestIm=TestIm*1
for k in range(W*H) :
    Si = k//W
    Sj = k%W   
        
    if TestIm[Si,Sj]== 1 and Si>kernSize and Sj>kernSize:
        print('Pixel:',Si,Sj)
        
        for tti in range(kernSize*2+1):
            for ttj in range(kernSize*2+1):
                MyPatch[tti][ttj]=TestIm[Si-kernSize+tti][Sj-kernSize+ttj]
            print(MyPatch[tti])
            
        TestIm[Si,Sj]= 0
        ConnectID=[]
        #--- This loop extracts the adjacent pixels for Si,Sj
        for dk in [1,W-1,W,W+1]:
            Ei = (k+dk)//W 
            Ej = (k+dk) %W
            if TestIm[Ei,Ej]== 1 :
                ConnectID.append([k,k+dk])
                TestIm[Ei,Ej]= 0        
        
        while ConnectID:        
            Ei = ConnectID[0][-1]//W
            Ej = ConnectID[0][-1] %W
            ii = [tt//W-Si for tt in ConnectID[0]]
            jj = [tt %W-Sj for tt in ConnectID[0]]            
            LL = np.sqrt((ii[-1])^2+(jj[-1])^2)
            TT = np.arctan2(ii,jj)
            #print(ii,'\n',jj,'\n',TT)       
            Ang = np.mean(TT)
            Ai = int(round((LL+1)*np.sin(Ang)+Si))
            Aj = int(round((LL+1)*np.cos(Ang)+Sj))
            NextPix = [0,0,0]               
            for Ni in range(Ai-1,Ai+1):
                for Nj in range(Aj-1,Aj+1):
                    if TestIm[Ni,Nj]==1 :
                        print(Si,Sj,'\n',Ei,Ej,'\n',Ni,Nj,'\n')
                        Wtest = abs(np.cross([Ni-Si,Nj-Sj],[Ei-Si,Ej-Sj]))/np.sqrt((Ei-Si)^2+(Ej-Sj)^2)
                        if Wtest>NextPix[0]:
                            NextPix = [Wtest,Ni,Nj]
                            
            print(NextPix[1]*W+NextPix[2])
            ConnectID[0].append(NextPix[1]*W+NextPix[2])
            TestIm[Ni,Nj]= 0
                         
                
            if NextPix ==0:            
                LineData.append([ii[0],jj[0],ii[-1],jj[-1]])
                ConnectID.pop(0)
                print('Line:',LineData[-1])
        
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
