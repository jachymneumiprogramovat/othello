# Uživatelská dokumentace pro hru Othello

Hra Othello vznikla jako zápočtový projekt pro předmět NMIN112 - Programování
2. Umožňuje jak 1v1 offline multiplayer tak hru proti automatizovanému
protivníkovi.

## Instalace

### Baličky
Nezbytné balíčky pro spuštěný této hry jsou
 - Pygame
 - Pygame_gui
 - NumPy
 - Loguru
 - tqdm
### Spuštění
 Hru spustíte příkazem `python meta_main.py`

## Hraní

### Herní módy
Po spuštění hry dostanete na výběr ze dvou již zmíněných herních módů. Po
zvolení jednoho z nich se automaticky dostanete do hry ze které se dá vrátit
jen zavřením a spuštěním celého programu.

### Jak hrát?
Hru začíná vždy hráč s černými kameny. Možné tahy hráče který je
právě na řadě označují průsvitné žluté kameny. Při kliknutí na nepovolené políčko se
nic neděje a hra čeká dál na tah stejného hráče.

Nové kameny můžete pokládat jen tam kde společně s nějakým dřívějším vaším
kamenem uzavřou mezi sebou souvislou posloupnost kamenů nepřítele (směrů
uvažujeme všech osm).

### Obtížnost AI
Automatizovaný protivník je řešen algoritmem Monte-Carlo tree search. Jak
rychle vám bude odpovídat závisí na vašem procesoru a hodnotách
`SIMULATION_COUNT` a `ROLLOUT_COUNT` v souboru `ai/mts_constants.py`. Čím větší
budou tyto hodnoty tím pomalejší bude hra s AI, ale tím lepší protivník bude. 

Počáteční hodnoty jsou 100 a 5, což tvoří ideálního protivníka pro začátečníky
v Othellu. Pokud byste si chtěli navýšit obtížnost a nevadí vám si počkat tak
doporučujeme do souboru `ai/mts_constants.py` zavítat a tyto hodnoty změnit.
Stejné doporučení máme pokud se snažíte hrát na bramboře nebo pokud neoplýváte
trpělivostí.

### Konec hry
Hra končí pokud jeden z hráčů nemá už žádné kameny, nebo pokud ani jeden z
hráčů nemá žádný možný tah (nejčastěji se stává, že se zaplní celé pole). V
každém případě hru vyhrává ten hráč který má na konci více kamenů. Tento
výsledek si můžete přečíst v konzoli po skončení hry.


