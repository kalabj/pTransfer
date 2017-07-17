# pTransfer
Nástroj na kopírování agendy předávané skrze sdílený disk. Klient vkládá dotazy do připravené složky, ty jsou pomocí pTransferu přeneseny na interní disk Poskytovatele, kde je zpracují pracovnící. Odpovědi jsou poté pTransferem přeneseny zpět na sílený disk.


# Sdílený disk

Klient předává dva typy dokumentů, které ukládá do separé položek označené jako "Data X" a "Data Y".

```
ROOT
|
└───Data X
│   │
│   └───Dotazy
│   │   │   file021.xls
│   │   │   file021.pdf
│   │   
│   └───Odpovedi
│        │   file021.xls
│
└───Data Y
    │
    └───Dotazy
    |   │   file022.xls
    |   │   file022.pdf
    │   
    └───Odpovedi
        │   file022.xls
```   

# Interní disk
Data na interním disku jsou rozdělena podle dnů a měsíců tak, jak je script zpracoval. PDF přílohy jsou uložený do speciální složky.

```
ROOT
|
└───Data X
│   │
│   └──Dotazy
│   |  |
|   |  └── MM_YYYY
|   |      |
|   |      └── DD_MM
|   |          |
|   |          └── PDF
|   |          │   │   file022.pdf   
|   |          │ file021.xls
|   |          | file022.xls
|   |
|   └──Odpovedi
│      |
|      └── MM_YYYY
|          |
|          └── DD_MM
|              |
|              └── ready2send
|              |   │ file021.xls
|              |   | file022.xls
|              |
|              └── sent
|                  │ file021.xls
|                  | file022.xls
|   
└───Data Y
    │
    └──Dotazy
    |  |
    |  └── MM_YYYY
    |      |
    |      └── DD_MM
    |          |
    |          └── PDF
    |          │   │   file022.pdf   
    |          │ file021.xls
    |          | file022.xls
    |
    └──Odpovedi
       |
       └── MM_YYYY
           |
           └── DD_MM
               |
               └── ready2send
               |   │ file021.xls
               |   | file022.xls
               |
               └── sent
                   │ file021.xls
                   | file022.xls

```  

# Scénář

1. stažení dotazů
1. jsou-li nové soubory, tak vytvoření příslušných adresářů
1. odeslání odpovědí ze složek **ready2send**, odeslané soubory jsou přesunuty do složky **sent**
1. notifikace o provedených úkonech

# Další funkce

* logování jednotlivých kroků, záznamy typu INFO, WARNING a ERROR
* v případě chyby odeslání notifikace
