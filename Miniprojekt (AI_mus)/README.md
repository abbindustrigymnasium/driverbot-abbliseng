# Miniprojekt
Mitt miniprojekt heter AI_mouse och är basserat på instruktionerna i denna länk. Jag valde först att följa instruktionerna och sedan med den nya kunskapen skapa ett eget program med samma mål och utgångspunkt. Musens beetende är inte hårdkodat utan den väljer sitt nästa steg utifrån en mängd vikter som tillhör varje möjlig ruta. Den väljer rutan med längst vikt (sys tydligast i debug mode) och lämnar samtidigt ett spår efter sig.  
  
Musens mål är att ta sig till osten vars effekt/lukt ökar med jämna mellanrum, detta innebär att musen alltid hittar osten tillslut (om ej överlevnadsläget är på då musen kan "dö" om den för slut på energi). Om musen lyckas äta osten (stå på samma ruta) skapas en ny ost på ett slumpat ställe och effekten av den tidigare osten och musens spår försvinner.
## Kör projektet
Efter att ha laddat ner filerna behöver du bara starta och köra filen **AI-Mus_finished_project**.
## Inställningar
![Image of size setting](https://github.com/abbindustrigymnasium/driverbot-abbliseng/blob/master/Miniprojekt/pictures/window_size.PNG)  
![Image of map size setting](https://github.com/abbindustrigymnasium/driverbot-abbliseng/blob/master/Miniprojekt/pictures/map_size.PNG)  
![Image of player/cheese setting](https://github.com/abbindustrigymnasium/driverbot-abbliseng/blob/master/Miniprojekt/pictures/player_cheese.PNG)  
**Survival Mode**  
![Image of survival code](https://github.com/abbindustrigymnasium/driverbot-abbliseng/blob/master/Miniprojekt/pictures/survival.PNG)  
**Normal Mode**  
![Image of normal code](https://github.com/abbindustrigymnasium/driverbot-abbliseng/blob/master/Miniprojekt/pictures/normal.PNG)  
## Pseudokod/Plannering
### Grov utmålning
Målet är att skapa ett rutnät men en eller flera spelare samt matbitar. Spelarna tar steg utifrån vikter som tillhör varje ruta för att alltid gå till den rutar som tjänar dem bäst. Det kostar energi att ta steg och den återställs om spelaren lyckas äta maten. En möjlighet att göra att det inte drar energi ska finnas. Knappar i spelet för att se Debug ska finnas för enklare utveckling och även knappar för att lägga till spelare och mat. I debug ska man kunna se rutornas vikt så man kan avgöra om allt är som det ska. Den ska vara anpassningsbar så man ska kunna skriva in hur stor spelplanen och fönstret ska vara samt hur fort/långsamt spelarna rör sig och hur mycket energi varje steg tar.
### Pseudokod
* Skapa en blueprint för "världen"/ ett rutnät med angiven storlek.  
* Skapa ett fönster i Tkinter och rendrera ett rutnät efter blueprinten där varje ruta har ett ID. (med fin färg! :) )
* Skapa en spelare och en mus ifrån klasser.  
* Spelaren ska vid varje loop kolla på sina närmaste rutor och gå till den som ger mest (längst vikt som tillhör den rutans ID). Om * ingen enskild ruta är att föredra; slumpa en ruta.  
* Var 10de steg ska osten minska vikten på rutorna i en diamant runt sig och därmed göra att spelaren föredrar dessa rutor.  
* Om spelaren står på samma ruta som maten, ta bort maten och återställ rutornas vikter till ett ursprungsvärde och slumpa en ny ruta att skapa mat på. Det ska alltså alltid finnas lika många matbitar.
* Efter en spelare gått ett steg ökas vikten på tidigare steg för att undvika att spelaren går bakåt.
* * Detta spår avtar med ett visst värde för varje steg, detta skapar ett spår efter musen. (Skapas genom att multiplicera vikten men ett procentuellt värde till det är under "normal" vikten då den tas bort från listan över "spår rutor".
* Processen av att ta ett steg och "äta" sker i en loop för alla spelare.
### Överlevnadsläge
* I överlevnadsläge förlorar spelaren 1 energi för varje steg och börjar med ett angivet värde energi.
* Om spelaren äter en matbit återställs energi nivån och spelet fortsätter som vanligt.
* Om spelaren får slut på energi innan den lyckas äta en matbit "dör" spelaren och objektet förstörs.
* Om inga spelare finns kvar på spelplanen stängs spelet.
### Normalt läge
* I normalt läge dras ingen energi och musen fortsätter att ta steg förevigt.
### Extra
* Knapp för att lägga till/ta bort spelare.
* * Skapar/Tar bort ett objekt av klassen spelare.
* Knapp för att lägga till/ta bort mat.
* * Skapar/Tar bort ett objekt av klassen mat.
* Knapp för att visa debug.
* * Om knappen trycks växlar ett värde mellan True och False.
* * Om True målas rutorna i en röd nyans men hänsyn till deras vikt.
* * Om en ruta ej kan målas (invalid färgvärde) blir den angiven en tydlig färg.
* * Denna karta över vikter ska uppdateras för varje steg spelaren tar.
* Knapp för att pausa spelet.
* * Växlar ett värde mellan True och False
* * Om True ska endast skärmen uppdateras (den loopar alltså inte igenom spelarna längre och därmed verkar spelet pausat.
* * Om False loopas spelarna igenom.

## Kända buggar/fel som finns och eventuell lösning
* Musen cirklulerar ibland osten utan att äta den.
* * Detta beror på att den ibland beräknar ostens vikt fel och att närliggande rutor anses bättre. Ska vara löst nu (2020-05-11).
* Om flera möss måste mössen vänta på att tidigare möss rört sig innan den kan röra sig (turn)
* * För att lösa detta kan man skapa en thread för varje mus rörelse.
