function pozicije=pronalazak_brojeva(stat, img_kon)
%{
Funkcija sprema 81 polje za igru
Ulaz:
    pts- vraæa toèke za 81 polje 
    stats - podatke o objektima

%} 
t=[];
%izvlaèenje središta
for i=1:81
    t(i,:)=stat(i).Centroid;
end

%slaganje po y
quick_y=quicksort(t(:,2));
for i=1:81
    for j=1:81
        if quick_y(i)==stat(j).Centroid(2)
            novi_stat(i)=stat(j);
            stat(j).Centroid(2)=0;
            break;
        end
    end
end

% sada su brojevi složeni po y po redovima, 9 redova*(9 sliènih)
kmin=1;
kmax=9;
k_slozeno=1;

while 1
    i=1;
    t=[];
    for k=kmin:kmax
        t(i,:)=novi_stat(k).Centroid;
        i=i+1;
    end
    quick_x=quicksort(t(:,1));
    for i=1:9
        for j=kmin:kmax
            if quick_x(i)==novi_stat(j).Centroid(1)
                poslozeni_stat(k_slozeno)=novi_stat(j);
                stat(j).Centroid(1)=0;
                k_slozeno=k_slozeno+1;
                break;
            end
        end
    end
    
    kmin=kmin+9;
    kmax=kmax+9;
    if kmin>=81
        break
    end
end

for i=1:81
    
    DIAG1 = sum(poslozeni_stat(i).PixelList,2);
    DIAG2 = diff(poslozeni_stat(i).PixelList,[],2);

    [m,dUL] = min(DIAG1);
    [m,dDR] = max(DIAG1);
    [m,dDL] = min(DIAG2);
    [m,dUR] = max(DIAG2);
    
    pts2 = poslozeni_stat(i).PixelList([dUL dDL dDR dUR dUL],:);

    yk=max(pts2(:,2));
    yp=min(pts2(:,2));
    xk=max(pts2(:,1));
    xp=min(pts2(:,1));
    nova=img_kon(yp:yk,xp:xk);   
    img_nova=imresize(nova,[600 600],'bilinear');

    [~, maxArea, stat]=pronalazak_polja(img_nova,[]);
    
    if maxArea>300*150
        yk=ceil(stat.BoundingBox(2)+stat.BoundingBox(4));
        yp=ceil(stat.BoundingBox(2));
        xk=ceil(stat.BoundingBox(1)+stat.BoundingBox(3));
        xp=ceil(stat.BoundingBox(1));      
        nova=img_nova(yp:yk,xp:xk);   
    else
        nova=img_nova(50:(600-50),50:(600-50));
    end
    %{
    figure(10)
    subplot(1,2,1)
    imshow(img_nova)
    rectangle('Position',[stat.BoundingBox(1),stat.BoundingBox(2),stat.BoundingBox(3),stat.BoundingBox(4)],...
                'EdgeColor','y','LineWidth',2 )
    subplot(1,2,2)
    imshow(nova)
    %}
    img_nova=imresize(nova,[600 600],'bilinear');
    pozicije{i}=img_nova;   
end
end