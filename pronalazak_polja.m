function [pts, maxArea, stat] = pronalazak_polja(BW,povrsina_zadana)
%{
Cilj:
    pronaæi polje za igranje

Ulaz:
    BW - binarna slika
Izlaz:
    pts-4 krajnje toèke polja
    maxArea-velièina polja u pikselima
    stat-
        returns measurements for the set of properties 
        specified by properties for each 8-connected component (object)
        in the binary image, BW. stats is struct array
        containing a struct for each object in the image.

%}
if isempty(povrsina_zadana)
    gornja_granica=1000000;
    donja_granica=5000;
else
    gornja_granica=(povrsina_zadana+5000);
    donja_granica=povrsina_zadana/3;
end;


%Inverzna slika
BW_I = ~BW;

%pronalaženje svih objekata i njihovih obilježja
[B,L,N,A] = bwboundaries(BW_I);
STATS = regionprops(L, 'all');

%{
figure
imshow(BW); hold on;

colors=['b' 'g' 'r' 'c' 'm' 'y'];
j=1;
%}
kmax=0;
maxArea = 0;

% PRONALAZAK POLJA

for i = 1:length(STATS)

    if (STATS(i).Area<gornja_granica && STATS(i).Area>donja_granica)
          
          %{
          boundary = B{i};
          %plot(boundary(:,2), boundary(:,1),'r--','LineWidth',2);
          hold on
          plot(STATS(i).Centroid(1), STATS(i).Centroid(2), 'b*');
          hold on
          plot(ceil(STATS(i).BoundingBox(1)), ceil(STATS(i).BoundingBox(2)), 'r*');
          hold on
          plot(1, 1, 'g*');
          
          cidx = mod(i,length(colors))+1;
          plot(boundary(:,2), boundary(:,1),...
               colors(cidx),'LineWidth',2);

          %randomize text position for better visibility
          rndRow = ceil(length(boundary)/(mod(rand*i,7)+1));
          col = boundary(rndRow,2); row = boundary(rndRow,1);
          h = text(col+1, row-1, num2str(L(row,col)));
          set(h,'Color',colors(j),'FontSize',14,'FontWeight','bold');
          j=j+1;
          
          rectangle('Position',[STATS(i).BoundingBox(1),STATS(i).BoundingBox(2),STATS(i).BoundingBox(3),STATS(i).BoundingBox(4)],...
'EdgeColor','y','LineWidth',2 )
          %}
          if STATS(i).Area > maxArea
            maxArea = STATS(i).Area;
            kmax = i;
            A = prod(STATS(i).BoundingBox(3:4));
          end
    end
end
if kmax==0
    %fprintf('Nema stvari nikakvih\n');
    stat=[];
    pts=0;
    maxArea=0;
    return
end
%PRONALAZAK TOÈAKA

%Area-
%BoundingBox (a-poèetna toèka x, b poèetna y, c-duljina po x, d-duljina po y )
%toèke nije moguæe tražiti direktno preko BoundingBoxa jer on daje samo x0
%y0 i dx i dy
DIAG1 = sum(STATS(kmax).PixelList,2);
DIAG2 = diff(STATS(kmax).PixelList,[],2);

[m,dUL] = min(DIAG1);
[m,dDR] = max(DIAG1);
[m,dDL] = min(DIAG2);
[m,dUR] = max(DIAG2);
pts = STATS(kmax).PixelList([dUL dDL dDR dUR dUL],:);
stat=STATS(kmax);
end