function pozicije = polje(img)
%{
Funkcija kao ulazni prima sliku sudoku polja, 
a vraæa 81 malu sliku u obliku cell

ULAZ:
    slika-img
        [img, map] = imread('slika2b.png');
        [img, map] = imread('slika3.png');
IZLAZ:
    pozicije-zasebne slike brojeva 
        81*(600x600)
        

PRIMJER POZIVA:

[img, map] = imread('slika2b.png');
pozicije=polje(img)

%}

%clc 
%clear all
%[img, map] = imread('slika2b.png');
%[img, map] = imread('slika3.png');
        

% RGB -> GRAY
img_gray=rgb2gray(img);

%{
% ISPIS

% figure(1)
% subplot(1,2,1)
% imshow(img)
% title('Original')
% subplot(1,2,2)
% imshow(img_gray)
% title('Siva slika')
%}




level1 = graythresh(img_gray);
TRESH1 = im2bw(img_gray,level1);
%PROBLEM : 
%       kako savršeno s pomoæu filtra obraditi sliku
%      UREÐIVANJE SLIKE 
%      širina koju prošušta

%level2 = graythresh(GAUS);
%GAUS=imgaussfilt(img_gray, 0.5);
%TRESH2 = im2bw(GAUS,level2);
% http://www-rohan.sdsu.edu/doc/matlab/toolbox/images/strel.html

%PROBLEM:
%       KAKO KVALITETNO OBRADITI SLIKU
%       pronalazak dobrog oblika za jako lošu sliku
% se = strel('square',2);
% SE = strel('disk',3,4);
% SE = strel('diamond',2);
% erodeI=imerode(TRESH2,se);


%{ 
ISPIS
% figure(2)
% subplot(2,2,1)
% imshow(TRESH1)
% title('Binarna slika bez filtriranja gausom')
% subplot(2,2,2)
% imshow(TRESH2)
% title('Binarna slika nakon filtriranja gausom')
% subplot(2,2,3)
% imshow(erodeI)
% title('Binarna slika nakon funkcije erode')
%}
% u ovom sluèaju uzimamo obiènu binarnu dobivenu iz sive originalne slike
%moguæa pobolješanja tu ili na kraju
BW=TRESH1;

% U funkciju šaljemo crno bijelu sliku a nazad dobivamo 4 toèke polja za
% igru i površinu u pikselima

[pts1,maxArea1,stat2]=pronalazak_polja(BW, []);

%TRANSFORMACIJA
%   iskrivljene slike u pravilnu funkcionira i kada je slika
%   pravilno postavljena
fixedpoints = [0 0; 200 0; 200 200; 0 200];
movingpoints= [pts1(1:4,1),pts1(1:4,2)];
transformationtype='projective';
tform = fitgeotrans(movingpoints,fixedpoints,transformationtype);
imagepr = imwarp(BW,tform);

[pts2,maxArea2, stat]=pronalazak_polja(imagepr,maxArea1);
       
yk=max(pts2(:,2));
yp=min(pts2(:,2));
xk=max(pts2(:,1));
xp=min(pts2(:,1));
img_kon=imagepr(yp:yk,xp:xk);       

figure(5)
subplot(1,2,1)
imshow(img)
title('Original')
subplot(1,2,2)
imshow(img_kon)
title('Nakon obrade')

%%
% Pronalazak brojeva
stat=pronalazak_brojeva(img_kon,(yk-yp)*(xk-xp));

%%
pozicije=ispis( stat, img_kon);

%%
for i=1:81
    
    figure(6)
    hold on
    subplot(9,9,i)
    imshow(pozicije{i})
    
end
%% PROBLEM 
%       ostaje jedino obraditi sliku


%{


figure(6)
imshow(img_kon)

%   Pristup svakoj od 81 slike
img_nova=pozicije(81-i*9+n)

%%
%se1 = strel('square',25);
%se = strel('disk',2,4);
%se2 = strel('diamond',20);
A=ones(10,25)
se1 = strel(A);
se2=se1
dilateI=imdilate(img_nova,se1);
erodeI=imerode(img_nova,se1);

basic_gradient = imdilate(img_nova, se1) - imerode(img_nova, se2);

figure(8)
subplot(2,3,1)
imshow(img)
title('original')
subplot(2,3,2)
imshow(img_kon)
title('original ispravljen')
subplot(2,3,3)
imshow(img_nova)
title('proširena')
subplot(2,3,4)
imshow(erodeI)
title('pojaèana')
subplot(2,3,5)
imshow(dilateI)
title('oslabljena')
subplot(2,3,6)
imshow(basic_gradient)
title('oslabljena')
%}

end




%% MALO OBJAŠNJENJE ZA pronalaženje krajnjih toèaka
%{
https://www.mathworks.com/matlabcentral/answers/4358-regionprops
img = zeros(5,5);
img(2:4, 2:4) = 1;
props = regionprops(img, 'PixelList');
disp(img);
disp(props.PixelList);
    %}