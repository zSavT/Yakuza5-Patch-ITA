# Spiegazione Script
Lo script permette di tradurre in automatico tramite la libreria _deep_translator_ i file csv presenti nella cartella "_input_". Output dell'operazione è salvato nella cartella "_tradotto_".

## Struttura file

I file csv del gioco hanno il seguente formato:

```
INTEGER INTEGER TEXT
```
Esempio
```
293	326	Answer me.
2058	2177	You seem real tense.\nSomething happen?
```

La codifica dei file csv è "__UTF-16__".

## Problema

I caratteri speciali (come _\n_) alcune volte non vengono inseriti erroneamente.
