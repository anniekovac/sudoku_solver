ZADATAK: Unutar mape testovi nalazi se "test.mat" koji je potrebno povezati s pythonom, te se nalazi i "slika1"
	čiji je put potrebno proslijediti iz pythona u matlab skriptu "test.m" te izvršiti sve i vratiti matricu
	9x9, 
	možda skriptu "test.m" pretvoriti u matlab funkciju koja će primati put do slike, a vraćati matricu 9x9
	također unutar "test.m" su definirani svi putevi koje je također potrebno izvršiti kako bi se od bilo koje 
	mape mogla izvršavati skripta "test.m", ali i da se zna gdje se nalaze funkcije sve koje se pozivaju.



OPIS:

Mapa: Obrada_polja_i_prepoznavanje_brojeva

	mapa: analiza_slika - funkcije namijenjene za analizu slike
				ulaz-slika
				izlaz-matrica 9x9
	
	mapa: obrada_slika - funkcije namijenjene za obradu slike
				ulaz-slika
				izlaz- 81 slika

	mapa: trening     - namijenjena za stvaranje skup znacajki za svaki broj
			  - nakon stvaranja novog seta iz trainset.mat (hrpa slika brojeva 1,...9)
				stvorene setove podataka o znacajkama u .mat (data1, ..., data9) 
				obliku potrebno prebaciti u mapu analiza_slika
				gdje se nalazi osnovni set znacajki
			  - nije nužno pokretati vec se nalazi osnovi dataSet.mat u mapi analiza_slika

	mapa: testovi  - u njoj se nalaze slike za koje je ispravno napravljena analiza za osnovni skup znacajki
			koji se nalazi u mapi analiza_slika i naziva se dataSet.mat 
			
			-u njoj sadržana i mapa "testne slike za detekciju polja" 
			koji su namijenjene za testiranje prepoznavanje polja samoga, ne i analiza slika i 
			prepoznavanje brojeva
