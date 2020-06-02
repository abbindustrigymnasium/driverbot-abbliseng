# Driverbot
Uppgiften var med hjälp av lego, en node MCU, tt-motor och en servo m.m. konstruera en bil. Denna bli skulle sedan via en [hemsida](http://driverbot.s3-website-us-east-1.amazonaws.com/) styra bilen.  
### Planering  
Planen är att konstuera en bil utav lego och teknik komponenter. Skapa en hemsida av något slag och sedan kunna styra bilen via sagd hemsida.
* Anslut till MQTT-broker via angiven information (namn, topic, lösen m.m.)
* * Denna ska ej ansluta vid inladdning utav sida då detta motarbetar möjligheten att använda form för att byta vilken bil som styrs.
* Skicka paket från hemisida vid varje knapptryck (t.ex. 1:710:90)
* * Den första siffran avgör rikting, fram/bak. Den andra hastighet (testa möjliga värden som motorn orkar). Den tredje motsvarar sväningsriktningen då 90 grader är rakt fram.
* Mikrokontrollern på bilen ska uppfatta medelandet och genomgå följande process.
* * Dela upp värderna från medelandet.
* * Beräkna differensen i hjulhastighet mellan de två motorerna utifrån angiven svängradie.
* * Utifrån angiven riktning utför hastighetsförändringen och riktningsförändringen (kalla egen funktion som har hand om slutlig förändring).  

På hemsidan ska man kunna välja en topic att subscriba till också för lättare felsökning. Den ska inte ha en joystick som kontroll trots det kan vara mest användarvänligt då jag tycker det är tråkigt :((
## Frontend (Hemsida)
Hemsidan är en återskapning av den klassiska NES kontrollen av nintendo (lägg märke till att det står spetsen där det tidigare stått nintendo). 
![Image of site](https://github.com/abbindustrigymnasium/driverbot-abbliseng/blob/master/Miniprojekt/pictures/driverbot_hemsida.PNG)
Kontrollen består egentligen av tre delar; Vänstra delen, Mitten delen och den Högra delen.  
### Vänstra delen
Denna del består av de klassiska fyra pilarna; upp, ned, höger och vänster. Upp och ned ändrar bilens hastighet i motsvarande riktning och höger och vänsterpilarna dess styrning. Hastigheten ändras i steg av 10 men knapparna kan även hållas in för gradvis förändring.
## Backend (Mikrokontroller)
## Konstruktion
Konstruktionen av bilen har genomgått en rad generationer. Blev aldrig riktnigt nöjd men konstruktionen mestadels på grund av brist på material men känner att jag lyckats skapa det bästa möjliga med det jag hade tillgängligt. En förändring jag gjort ifrån första planering är att jag inte har någon form av differential mellan bakhjulen. För att undvika att den sladdar använder jag istället två TT motorer och uti från beräkningar av svängradie ändrar jag hastighets differensen mellan hjulen i svängarna.
# Miniprojekt
Mitt miniprojekt heter AI_mouse och är basserat på instruktionerna i denna länk. Jag valde först att följa instruktionerna och sedan med den nya kunskapen skapa ett eget program med samma mål och utgångspunkt. Musens beetende är inte hårdkodat utan den väljer sitt nästa steg utifrån en mängd vikter som tillhör varje möjlig ruta. Den väljer rutan med längst vikt (sys tydligast i debug mode) och lämnar samtidigt ett spår efter sig.  
  
Musens mål är att ta sig till osten vars effekt/lukt ökar med jämna mellanrum, detta innebär att musen alltid hittar osten tillslut (om ej överlevnadsläget är på då musen kan "dö" om den för slut på energi). Om musen lyckas äta osten (stå på samma ruta) skapas en ny ost på ett slumpat ställe och effekten av den tidigare osten och musens spår försvinner.

## Kända buggar/fel som finns och eventuell lösning
* Musen cirklulerar ibland osten utan att äta den.
* * Detta beror på att den ibland beräknar ostens vikt fel och att närliggande rutor anses bättre. Ska vara löst nu (2020-05-11).
* Om flera möss måste mössen vänta på att tidigare möss rört sig innan den kan röra sig (turn)
* * För att lösa detta kan man skapa en thread vid varje mus rörelse. (Inte implementerat)
