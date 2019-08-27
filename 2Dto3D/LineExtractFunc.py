'''
This function extracts the straight border lines of objects from an input image
Input: image of 2D drawing of a level of building
Output: Line properities (Start & End) in pixels
Developed by Meisam Yousefzadeh 9 April 2018
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

imgC = cv2.imread('PlanSample1.jpg',0)

#--- Main Program ---
edges = cv2.Canny(imgC,100,200)
plt.subplot(211)
plt.imshow(edges)

W = len(edges[0])
H = len(edges)
kernSize = 2
PP = -1

MyPatch= [[0 for x in range(kernSize*2+1)] for y in range(kernSize*2+1)]
#setattr(PixelAtt, 'foobar', 123)
#CorMap = [[0 for x in range(W)] for y in range(H)]
#LinMap = [[0 for x in range(W)] for y in range(H)]
LineData =[]
ConnectID=[]
TestIm = edges>0
TestIm=TestIm*1
for k in range(10*W,W*H) :
    Si = k//W
    Sj = k%W   
        
    if TestIm[Si,Sj]== 1 and Si>kernSize and Sj>kernSize:
        #print('Pixel:',k,Si,Sj)
        '''
        for tti in range(kernSize*2+1):
            for ttj in range(kernSize*2+1):
                MyPatch[tti][ttj]=TestIm[Si-kernSize+tti][Sj-kernSize+ttj]
            print(MyPatch[tti])
        '''    
        TestIm[Si,Sj]= 0
        NextPix = [0,0,0]
        #--- This loop extracts the adjacent pixels for Si,Sj
        for dk in [1,W-1,W,W+1]:
            Ni = (k+dk)//W 
            Nj = (k+dk) %W
            if Ni<H and Nj<W and TestIm[Ni,Nj]== 1 :
                PP = PP+1
                NextPix = [1,Ni,Nj]               
                ConnectID.append([k,k+dk])
                TestIm[Ni,Nj]= 0
                break
        
        while NextPix[1]>0:
            #print('last pointID:',ConnectID[-1][-1]//W,ConnectID[-1][-1] %W)
            Ei = ConnectID[-1][-1]//W               # End of line i(initial)
            Ej = ConnectID[-1][-1] %W               # End of line j(initial)
            ii = [tt//W-Si for tt in ConnectID[PP]] # coordinates for angle calc i
            jj = [tt %W-Sj for tt in ConnectID[PP]] # coordinates for angle calc j
            LL = np.sqrt((ii[-1])**2+(jj[-1])**2)   # Current length of line
            TT = np.arctan2(ii[1:],jj[1:])          # Azimute of each point regarding to (Ei,Ej)
            Ang = np.mean(TT)                       # Mean of Azimutes as the heading angle
            dAng = .5/LL                            # Angle tolerance to find the next candidate 
            Ai = [int(round((LL+1)*np.sin(Ang-dAng)))+Si, int(round((LL+1)*np.sin(Ang)))+Si,int(round((LL+1)*np.sin(Ang+dAng)))+Si] # Next 3 condidates i
            Aj = [int(round((LL+1)*np.cos(Ang-dAng)))+Sj, int(round((LL+1)*np.cos(Ang)))+Sj,int(round((LL+1)*np.cos(Ang+dAng)))+Sj] # Next 3 condidates j
            NextPix = [0,0,0]                       # initial for the next pixel
            Wtest = 0
            #--- this loop findes the best candidate which is closer to the current heading
            for tt in range(3):                     
                if Ai[tt]<H and Aj[tt]<W:
                    Ni=Ai[tt]
                    Nj=Aj[tt]
                    if TestIm[Ni,Nj]==1 :
                        Wtest = abs(np.dot([Ni-Si,Nj-Sj],[Ei-Si,Ej-Sj]))/(np.sqrt((Ni-Si)**2+(Nj-Sj)**2)*np.sqrt((Ei-Si)**2+(Ej-Sj)**2))
                        if Wtest>NextPix[0] and Ni*W+Nj!= ConnectID[-1][-1]:
                            NextPix = [Wtest,Ni,Nj]
                            
            #--- to introduce the winner condidate in the line data or close th line
            if NextPix[0]>0:
                #print(NextPix[1]*W+NextPix[2])
                ConnectID[-1].append(NextPix[1]*W+NextPix[2])
                TestIm[NextPix[1],NextPix[2]]= 0
            else:            
                LineData.append([Si,Sj,Ei,Ej])
                TestIm[Ei,Ej]= 0
                print('Line:',LineData[-1])

#--- to plot the lines
for tt in range(PP):
    plt.plot([LineData[tt][1],LineData[tt][3]],[LineData[tt][0],LineData[tt][2]])
plt.subplot(212)
plt.imshow(TestIm)
plt.show()
