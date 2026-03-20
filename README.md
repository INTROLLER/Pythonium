# Brute force-attacker för lösenord - Programkod och resultat

Detta är ett repository innehållande all programkod och rådata som användes i ett gymnasiearbete på teknisk linje under vårterminen 2026. Projektet syftade på att undersöka tidsåtgången och dess påverkan av olika lösenordsförhållanden under brute force-simuleringar. Anfall med ren Python och Hashcat har utförts.

## Innehåll
### Rotmappens innehåll
- main.py -- Huvudprogrammet som använts under experimentet. Kan köras i tre olika lägen: 
 -0: Enskilda testattacker på valfritt eller slumpat lösenord
 -1: Upprepade benchmarkmätningar samt ett medelvärde för dessa 
 -2: En komplett uppsättning av attacker mot en mängd lösenord i repots lösenordsmapp. (Det är i detta läge som rådata har tagits fram)
- hashcat.py -- Egentillverkad modul som huvudprogrammet använder för att anropa Hashcat under särskilda attacker.
- Övriga skript -- Hjälpprogram för hantering av rådata.

### Nedan beskrivs innehållet i repots undermappar.
/passwords/ -- Textfiler med alla lösenord som testats under experimentet.
/results/ -- En så kallad pickle-fil med rådata från experimentet. Kan extraheras med reader.py och visualiseras i ett spridningsdiagram med visualizer.py.

## Körning och krav
- Python version 3.11
- För attacker med Hashcat krävs installation av Hashcat version 7.1.2 placerad i rotmappen

## Etik
Genom att köra huvudprogrammet utförs simuleringar av attacker i en isolerad, kontrollerad testmiljö. Syftet med arbetet är inte att skapa ett kraftfullt verktyg för verkliga attacker, utan att undersöka vilken påverkan olika säkerhetsåtgärder har på lösenordens tider till   kompromettering. Körningar av huvudprogrammet mot verkliga lösenord uppmuntras inte.