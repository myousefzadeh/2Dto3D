tic;
%--- Initializations
ZI = uint8(255) - rgb2gray(imread('PlanSample3.jpg'));
%--- constant values
BinWidth = str2num(get(handles.SampleRes,'string'))/100; % Sampling resolution
PointDens = str2num(get(handles.PointNum,'string'));% number of points in each pixel
MinDist = str2num(get(handles.MinWinSize,'string'))/100; % Minimum acceptable Window dimention
AngleTol = str2num(get(handles.AngleThre,'string'))*pi/180; % Angle tolerance(degrees) for classification of anchor points
DistTol = MinDist/BinWidth; % Distance tolerance(Pixels) for line removal and corner detection
DistTol2 = 1.5/BinWidth; % Distance tolerance(Pixels) for Gap filling specially for door size 
WallTol = str2num(get(handles.WallZoneTre,'string'))/100/BinWidth; % Distance tolerance(Pixels) for wall patch dedetion
CurrentZone = str2num(get(handles.CurrentZone,'string')); % Zone number

%--- find and sort the data file based on point density in pixels
[Mi,Mj] = find(ZI>PointDens );
for kk=1:length(Mi)
    uuu(kk)=ZI(Mi(kk),Mj(kk));
end
%--- Sort the pixels based on point densities
[BB,XI]=sort(uuu,'descend'); 
Mi =Mi(XI);
Mj =Mj(XI);
FulPixel = uuu(XI); 
PixLab(XI) = 0;
Tet(length(Mj))=0;  Myb(length(Mj))=0; 
figure; imshow(ZI>PointDens)
%% --- Wall Line extraction process 
pp=0;
for i = 1:length(Mi)
    if  PixLab(i) == 0 % to avoid double caclulations
        MyW = []; 
        %--- folowing loop gives weigth to all directions  
        for j = 1:length(Mi)
            if  i~=j & PixLab(j) == 0
                if Mi(i)==Mi(j) 
                    Inlier = find(Mi==Mi(i));
                 else
                    MyAA= (Mi(i)-Mi(j))/(Mj(i)-Mj(j));
                    Inlier = find(abs(Mi-Mi(i)-MyAA*(Mj-Mj(i)))<1);
                end
                MyW(j) = sum(FulPixel(Inlier)); % Weights based on pixel values alonge the line
            end
        end
        [MymaxW,WjID] = sort(MyW,'descend'); % sort the weights
        kk = 1; EE1=0; EE2=0;
        while abs(EE2-EE1) < DistTol & isempty(WjID)==0 & MymaxW(kk)>0
            if  Mi(i)==Mi(WjID(kk)) % for vertical slop
                Inlier = find(Mi==Mi(i));
                allDists = Mj(Inlier)-Mj(i);
            else       % for nonvertical slop
                MyAA = (Mi(i)-Mi(WjID(kk)))/(Mj(i)-Mj(WjID(kk)));
                Inlier = find(abs(Mi-Mi(i)-MyAA*(Mj-Mj(i)))<1);
                allDists = Mi(Inlier)-Mi(i)+(1/MyAA)*(Mj(Inlier)-Mj(i));
            end
            [myDis, DisID] = sort(allDists);    % Sort the distances in order
            MaxID = find(myDis==0);             %The position of max point in the line
            DmyDis = [diff(myDis); 0];          % diferensials to detect gaps
            SS1 = find(DmyDis(1:MaxID)>DistTol);% find the first gap on the left
            %--- to detect the start point of the line
            if isempty(SS1); 
                EE1 = 1; 
            else
                EE1 = SS1(end)+1;
            end
            SS2 = find(DmyDis(MaxID:end)>DistTol);  % find the first gap on the right
            %--- to detect the end point of the line
            if isempty(SS2); 
                EE2=length(DisID); 
            else
                EE2 = SS2(1)+MaxID-1;
            end
            kk=kk+1;
        end
        if abs(EE2-EE1) > DistTol
            pp = pp+1;                                              % Line number
            inLinePix = EE1:EE2;                                    % The pixels located in the line
            NoLablePix = find(PixLab(Inlier(DisID(inLinePix)))==0); % Line pixels without label
            WeightInf(pp,:) = [EE1 MaxID EE2 sum(FulPixel(Inlier(DisID(inLinePix(NoLablePix))))) 0];   % Start,Pic and end pixels and the assigned weight
            LineX1 = Mj(Inlier(DisID(EE1))); LineY1 = Mi(Inlier(DisID(EE1)));       % Start coordinates of the line
            LineX2 = Mj(Inlier(DisID(EE2))); LineY2 = Mi(Inlier(DisID(EE2)));       % End coordinates of the line
            if LineY1==LineY2; LineTet = pi/2; LineB = LineY1; else LineTet = atan((LineY1-LineY2)/(LineX1-LineX2)); LineB = LineY1-tan(LineTet)*LineX1; end % Update the slope 
            MyLines(pp,:) = [LineX1 LineY1 LineX2 LineY2 LineTet*180/pi LineB 0 0]; % Line Info
            line([MyLines(end,1) MyLines(end,3)], [MyLines(end,2) MyLines(end,4)],'Color','y');
%             text(mean(MyLines(end,1), MyLines(end,3)),mean(MyLines(end,2), MyLines(end,4)),num2str(pp),'Color',[0 0 1], 'BackgroundColor',[.7 .9 .7]);
            PixLab(Inlier(DisID(inLinePix(NoLablePix))))=-pp;       % a primary line label to the pixels
        end
    end
end
%--- Sort the lines according to the height and line label for pixels
[LineW LineID] = sort(WeightInf(:,4),'descend');
WeightInf = WeightInf(LineID,:);
MyLines = MyLines(LineID,:);
for i=1:length(LineID)
    MyLiID = find (PixLab==-LineID(i));
    PixLab(MyLiID) = i;
end
WeightTre = max(WeightInf(:,4))/50;

%% --- Remove redundant lines, update the lines and detect a boundary of attached elements to the wall 
for i=1:length(MyLines(:,1))
    if WeightInf(i,5)==0
%         WeightInf(i,5) = 1;
        XX1 = MyLines(i,1); YY1 = MyLines(i,2); XX2 = MyLines(i,3); YY2 = MyLines(i,4);MyAngi = MyLines(i,5); MyAA = tan(MyAngi*pi/180); 
        AliP = find( (abs(MyLines(:,2)-YY1-MyAA*(MyLines(:,1)-XX1))<DistTol/3 & abs(MyLines(:,4)-YY1-MyAA*(MyLines(:,3)-XX1))<DistTol/3 & WeightInf(:,5) == 0)  ... % both points are in line area
                      |(abs(MyLines(:,2)-YY1-MyAA*(MyLines(:,1)-XX1))<DistTol/3 & abs(sin((MyLines(:,5)-MyAngi)*pi/180))<AngleTol & WeightInf(:,5)==0 )   ...  % point 1 in line area
                      |(abs(MyLines(:,4)-YY1-MyAA*(MyLines(:,3)-XX1))<DistTol/3 & abs(sin((MyLines(:,5)-MyAngi)*pi/180))<AngleTol & WeightInf(:,5)==0 ) );     % point 2 in line area                    
        %--- to connect almost parallel line segments
        if length(AliP)>1
            MyRR = [cos(MyAngi*pi/180) -sin(MyAngi*pi/180); sin(MyAngi*pi/180) cos(MyAngi*pi/180)];
            MyCo1 = [ MyLines(AliP(:),1) MyLines(AliP(:),2) ]; LLLs = MyCo1*MyRR; LLL1 = LLLs(:,1);%[1/MyAA ;1]-MyLines(i,1)/MyAA-MyLines(i,2);
            MyCo2 = [ MyLines(AliP(:),3) MyLines(AliP(:),4) ]; LLLe = MyCo2*MyRR; LLL2 = LLLe(:,1);%[1/MyAA ;1];
            mmmin = min([LLL1;LLL2]); MyLLL=[];
            MidLLL = mean([LLL1 LLL2],2)-mmmin+1;
            for j=1:length(LLL1)
                line([MyLines(AliP(j),1) MyLines(AliP(j),3)], [MyLines(AliP(j),2) MyLines(AliP(j),4)],'Color','y');
                MyLLL(floor(min([LLL1(j) LLL2(j)])-mmmin+1):floor(max([LLL1(j) LLL2(j)])-mmmin+1)) = 1;
            end
            FullID = find(MyLLL==1); yyy=[FullID 0]-[0 FullID]; 
            MyGap = find (yyy>DistTol2); 
            t1=1; t2=length(MyLLL);
            GapID1 = max(MyGap(find(MyGap<MidLLL(1))));
            GapID2 = min(MyGap(find(MyGap>MidLLL(1))));
            if isempty(GapID1)==0
                t1=GapID1+yyy(GapID1);
            end
            if isempty(GapID2)==0
                t2=GapID2;%+yyy(MyGap(GapID2);
            end
            ttt = find(MidLLL>t1 & MidLLL<t2 );
            MyCo = [MyCo1(ttt,:);MyCo2(ttt,:)];
            [mmmax2 maxID] = max([LLL1(ttt); LLL2(ttt)]);
            [mmmin2 minID] = min([LLL1(ttt); LLL2(ttt)]);
            %--- Lind Info update
            MyLines(i,1:2) = MyCo(minID,1:2);
            MyLines(i,3:4) = MyCo(maxID,1:2);
            if MyLines(i,2)==MyLines(i,4)
               LineTet = pi/2; LineB = MyLines(i,2); 
            else
               LineTet = atan((MyLines(i,2)-MyLines(i,4))/(MyLines(i,1)-MyLines(i,3))); LineB = MyLines(i,2)-tan(LineTet)*MyLines(i,1); 
           end
           MyLines(i,5:6) = [LineTet*180/pi LineB ]; % Line Info
           WeightInf(i,4) = sum(WeightInf(AliP(ttt),4)); % Waight allocation for the main line
    %        WeightInf(AliP(ttt),4)= 0; % remove the weight of previous line
           PixID=[];
           for jj=1:length(ttt)
               PixID = [PixID find(PixLab == AliP(ttt(jj)))]; % Detect the pixels with old label
           end
           PixLab(PixID)= i; % Change the labels to a new label
           WeightInf(AliP(ttt),5) = 3; WeightInf(i,5) = 1;
        end
       line([MyLines(i,1) MyLines(i,3)], [MyLines(i,2) MyLines(i,4)],'Color','b');
       text(mean([MyLines(i,1) MyLines(i,3)])+2,mean([MyLines(i,2) MyLines(i,4)])+2,num2str(i),'Color',[1 0 0], 'BackgroundColor',[.7 .0 .7]);

    end
end
%--- Sort the lines according to the higher waight
[LineW LineID] = sort(WeightInf(:,4),'descend');
WeightInf = WeightInf(LineID,:);
MyLines = MyLines(LineID,:);