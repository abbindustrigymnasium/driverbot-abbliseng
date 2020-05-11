# Main
## Miniprojekt
Mitt miniprojekt heter AI_mouse och är basserat på instruktionerna i denna länk. Jag valde först att följa instruktionerna och sedan med den nya kunskapen skapa ett eget program med samma mål och utgångspunkt. Musens beetende är inte hårdkodat utan den väljer sitt nästa steg utifrån en mängd vikter som tillhör varje möjlig ruta. Den väljer rutan med längst vikt (sys tydligast i debug mode) och lämnar samtidigt ett spår efter sig.  
  
Musens mål är att ta sig till osten vars effekt/lukt ökar med jämna mellanrum, detta innebär att musen alltid hittar osten tillslut (om ej överlevnadsläget är på då musen kan "dö" om den för slut på energi). Om musen lyckas äta osten (stå på samma ruta) skapas en ny ost på ett slumpat ställe och effekten av den tidigare osten och musens spår försvinner.

### Kända buggar/fel som finns och eventuell lösning
* Musen cirklulerar ibland osten utan att äta den.
* * Detta beror på att den ibland beräknar ostens vikt fel och att närliggande rutor anses bättre. Ska vara löst nu (2020-05-11).
* Om flera möss måste mössen vänta på att tidigare möss rört sig innan den kan röra sig (turn)
* * För att lösa detta kan man skapa en thread vid varje mus rörelse. (Inte implementerat)
# Extra
## Notes
1. (2020-03-31) Av någon anledning kan jag inte ladda upp ifrån github repon till esp:n så återgår till att ha det lokalt på datorn och laddar sedan upp när färdigt, dvs uppdaterar den nuvarande filen när esp koden är klar.
2. (2020-03-31) Jag har byggt om denna bil så så många gånger nu att jag häromed ger upp! (alltså inte på allt men på bilens utseende)
3. *Det va ingen rak linje tho men men...*
4. (2020-03-31) ESP koden är nu klar och uppladdad. Funderar dock över att byta vilka bibliotek som används senare då detta strullar ibland.
5. (2020-03-31) Väljer att göra en app då jag inte kan det ännu och skulle vilja lära mig.
## Logbok
### 2020-03-23
* Konstruering av bilplatfroms sak
* Ombyggnad av bil
### 2020-03-24
* Fortsatt konstruktion av bil
* Programering på mini projektet
### 2020-03-27
* Påbörjan av hemsida  
*PS redan gjort en men den behöver lite improvments. Det kan även bli så att det blir en app i slutändan.*
### 2020-03-31
* Fortsatt bygge av bil  
*Satsar på bra konstruktion och vill även lära mig hur man bygger bra så lägger extra tid här*
* Test av konstruktion och programmering av test sekvens
* Bygge av plats till powerbank istället för batterier  
*Det var här visionen om en bra och fin konstruktion dog.*
* Beräkning av svängradie mm för att optimera körning :)  
*Dokumentering kommer snart*
* Implementering av svängradie och anpassning av fart mellan de två hjulen beroende på hur den svänger.  
*Detta undviker att den slirar i svängar, valde även att inte använda en differential då jag tänkte att detta skulle vara roligare och mer lärorikt plus att bilen blir lite mer kompakt. Det kräver dock två motorer men samtidigt hjälper båda hjulen nu till i svängarna.*
### 2020-04-20
* Skapande av app för styrning.
* Byte till hemsida då expo-cli slutatde fungera efter uppdatering p.g.a. admin permissions. dvs kunde inte uppdateras korrekt och paja sig själv.
### 2020-04-21
* Arbete på hemsida  
*Väljer att ej ha en joystick då det verkar som nästan alla gjort det så tycker det blivit lite uttjatat plus att jag vill ha mer av en utmaning gällande hur man placerarar saker på specifika platser på skärmen (layout).*
### 2020-05-11
* Förberedelse inför redovisning och förfining av github sidan :)
