# Yakuza5-Patch-ITA
<p align="center">
  <img src="img/LogoYakuza5.png" /><br>
    Progetto per la traduzione del gioco Yakuza 5 REMASTEERED in italiano.
</p>

![GitHub contributors](https://img.shields.io/github/contributors/zSavT/Yakuza5-Patch-ITA)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/paypalme/verio12)


Il "progetto" è nato totalmente a caso e spinto dalla mia curiosità nel riuscire a modificare i testi del gioco, dopo aver provato la Patch per Yakuza 0 sviluppata da [Rulesless](https://letraduzionidirulesless.wordpress.com/yakuza0-2/). <br> La mia ricerca è iniziata cercando sul web, l'esistenza di altre patch di traduzioni in altre lingue, per poter analizzare la patch e comprendere più velocemente quali siano i file contenenti i testi del gioco.<br> Per questo motivo ho iniziato ad analizzare la [patch spagnola](https://steamcommunity.com/sharedfiles/filedetails/?id=3385318071) del gioco.<p>
Analizzando i file, mi sono occorto che principalmente il gioco utilizza file  _PAR_ e file _BIN_ (con varianti di quest'ultimi in alcuni casi).I file PAR contengono i principali dati del gioco (immagini, animazioni ecc...) e lo stesso vale per i file BIN. Su GitHub casualmente ho trovato alcune repo che permettono di scompattare e ricompattare questi file, in tal modo ho iniziato a comprendere come muovere i primi passi per la traduzione dei testi del gioco.

## Struttura dei file (Noti al momento)


- Yakuza 5\data\auth\subtitle.par
    - All'interno sono presenti tutti i testi per le cutscene presenti nel gioco.
    - [x] Tradotto ma da rivisionare
- Yakuza 5\data\2d
    - All'interno sono presenti la maggior parte delle grafiche del gioco.
    - [ ] Tradotto

# Funzionamento script

Lo script utilizza le api di Gemini 2.0 per poter funzionare. Le API al momento sono utilizzabili gratuitamente (per ora). La chiave si può ottenere da [qui](https://aistudio.google.com/apikey).<br>
Bisogna inserire la chiave all'interno del file "_traduttore_auto_csv/api_key.txt_" oppure lanciando lo script python tramite il flag "_--api [CHIAVE_API]_".
Ovviamente bisogna sostituire "_CHIAVE API_" con la propria chiave.

```
python .\main.py --api [CHIAVE_API]
```

## TO DO

- [x] Codifica e decodifica dei file PAR
- [ ] Codifica e decodifica dei file BIN (Controllando questa [repo](https://github.com/SlowpokeVG/Yakuza-2007.03.19-bin-file-exporter-importer), i file relativi a Yakuza 4 non sembrano compatibili, testando con altri giochi della serie si)

## Dipendenza

Per la codifica e la decodifica dei file _PAR_ del gioco, si utilizza il programma sviluppato nella [repo](https://github.com/Kaplas80/ParManager.git) da Kaplas80.
