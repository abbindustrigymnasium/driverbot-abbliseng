# Main
## Driverbot
Uppgiften var med hjälp av lego, en node MCU, tt-motor och en servo m.m. konstruera en bil. Denna bli skulle sedan via en [hemsida](http://driverbot.s3-website-us-east-1.amazonaws.com/) styra bilen.  
**Planering**

### Frontend (Hemsida)
### Backend (Mikrokontroller)
### Konstruktion
Jag valde att använda två tt motorer för att sedan 
## Miniprojekt
Mitt miniprojekt heter AI_mouse och är basserat på instruktionerna i denna länk. Jag valde först att följa instruktionerna och sedan med den nya kunskapen skapa ett eget program med samma mål och utgångspunkt. Musens beetende är inte hårdkodat utan den väljer sitt nästa steg utifrån en mängd vikter som tillhör varje möjlig ruta. Den väljer rutan med längst vikt (sys tydligast i debug mode) och lämnar samtidigt ett spår efter sig.  
  
Musens mål är att ta sig till osten vars effekt/lukt ökar med jämna mellanrum, detta innebär att musen alltid hittar osten tillslut (om ej överlevnadsläget är på då musen kan "dö" om den för slut på energi). Om musen lyckas äta osten (stå på samma ruta) skapas en ny ost på ett slumpat ställe och effekten av den tidigare osten och musens spår försvinner.

### Kända buggar/fel som finns och eventuell lösning
* Musen cirklulerar ibland osten utan att äta den.
* * Detta beror på att den ibland beräknar ostens vikt fel och att närliggande rutor anses bättre. Ska vara löst nu (2020-05-11).
* Om flera möss måste mössen vänta på att tidigare möss rört sig innan den kan röra sig (turn)
* * För att lösa detta kan man skapa en thread vid varje mus rörelse. (Inte implementerat)
