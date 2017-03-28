function stat = pronalazak_brojeva(BW,povrsina_zadana)

%{
Funkcija pronalazi sva igraæa polja
ako ne naðe 81 polje baci error
Ulaz:
    BW- binarna slika 
    povrsina_zadana - pretpostavljena velièina polja
Izlaz:
    pts- vraæa toèke za 81 polje 
    stats - podatke o objektima

%}    
gornja_granica=ceil(povrsina_zadana/50);
donja_granica=ceil(povrsina_zadana/170);
%donja_granica=ceil(povrsina_zadana/110)

BW_I = ~BW;

%pronalaženje svih objekata i njihovih obilježja
[B,L,N,A] = bwboundaries(BW_I);
STATS = regionprops(L, 'all');

%figure
%imshow(BW); hold on;
%colors=['b' 'g' 'r' 'c' 'm' 'y'];

j=1;
kmax=0;

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
        set(h,'Color',colors(1),'FontSize',14,'FontWeight','bold');


        rectangle('Position',[STATS(i).BoundingBox(1),STATS(i).BoundingBox(2),STATS(i).BoundingBox(3),STATS(i).BoundingBox(4)],...
            'EdgeColor','y','LineWidth',2 )
%}
        
        stat(j)=STATS(i);
        kmax=kmax+1;
        j=j+1;
    end
end

if kmax ~= 81
    msg = 'Nisu pronaðena sva polja, potrebno je podesiti granice';
    error(msg)
end



end