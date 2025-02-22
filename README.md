# Yakuza4-Patch-ITA
![GitHub contributors](https://img.shields.io/github/contributors/zSavT/Yakuza4-Patch-ITA)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/paypalme/verio12)


Il "progetto" è nato totalmente a caso e spinto dalla mia curiosità nel riuscire a modificare i testi del gioco, dopo aver provato la Patch per Yakuza 0 sviluppata da [Rulesless](https://letraduzionidirulesless.wordpress.com/yakuza0-2/). <br> La mia ricerca è iniziata cercando sul web, l'esistenza di altre patch di traduzioni in altre lingue, per poter analizzare la patch e comprendere più velocemente quali siano i file contenenti i testi del gioco.<br> Per questo motivo ho iniziato ad analizzare la [patch spagnola](https://steamcommunity.com/sharedfiles/filedetails/?id=3385318071) del gioco.<p>
Analizzando i file, mi sono occorto che principalmente il gioco utilizza file  _PAR_ e file _BIN_ (con varianti di quest'ultimi in alcuni casi).I file PAR contengono i principali dati del gioco (immagini, animazioni ecc...) e lo stesso vale per i file BIN. Su GitHub casualmente ho trovato alcune repo che permettono di scompattare e ricompattare questi file, in tal modo ho iniziato a comprendere come muovere i primi passi per la traduzione dei testi del gioco.

## Struttura dei file (Noti al momento)


- Yakuza 4\data\auth\subtitle.par
    - All'interno sono presenti tutti i testi per le cutscene presenti nel gioco.
    - [x] Tradotto 
- Yakuza 4\data\hact\subtitle.par
    - All'interno sono presenti tutti i testi non presenti nelle cutscene o nei classi box di dialogo o menu.
    - [x] Tradotto 
- Yakuza 4\data\2d\cse_en.pa
    - All'interno sono presenti la maggior parte delle grafiche del gioco, in particolare quelle per l'immagine di introduzione dei capitoli e degli obbiettivi.
    - [ ] Parzialmente tradotto 
- Yakuza 4\data\2d
    - All'interno sono presenti la maggior parte delle grafiche del gioco.
    - [ ] Parzialmente tradotto 

## TO DO

- [x] Codifica e decodifica dei file PAR
- [ ] Codifica e decodifica dei file BIN (Controllando questa [repo](https://github.com/SlowpokeVG/Yakuza-2007.03.19-bin-file-exporter-importer), i file relativi a Yakuza 4 non sembrano compatibili, testando con altri giochi della serie si)

## Dipendenza

Per la codifica e la decodifica dei file _PAR_ del gioco, si utilizza il programma sviluppato nella [repo](https://github.com/Kaplas80/ParManager.git) da Kaplas80.
