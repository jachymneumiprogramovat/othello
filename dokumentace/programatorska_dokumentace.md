# Programátorská dokumentace

Toto je technicka dokumentace pro zápočtový projekt. Jedná se o podrobné
popsání důležitých funkcí a koncepce celého programu.

# Koceptuální režie programu
## Úvodní obrazovka
Celý program začíná v souboru `meta_main.py`, tam se vykreslí úvodní obrazovka
s tlačítky pomocí knihovny `pygame_gui`. Ty následně zpustí ten správný herní
cyklus odpovídající vybranému hernímu módu. 

## Herní cyklus
Na začátku hry inicializují všechny důležité třídy - jak ty grafické tak ty
logické. Herní cyklus se poté skládá z:
 - vyčkání na tah hráče nebo AI,
 - zapsání tohoto tahu do pole reprezentující herní plochu,
 - vyhodnocení konce hry a případné ukončení cyklu,
 - prohození aktuálního hráče
 - generování možných tahů (budou vykresleny jako možné pro soupeře),
 - vykreslení všech akcí na obrazovku (musí se překreslit možné tahy z minulého tahu).

# Hra Othello
Celá herní logika je v souboru `game/board.py` zatímco vykreslování je v
`game/game.py`. Každá z těchto částí má svojí třídu, společně s menší třídou
pro herní kámen to jsou všechny třídy ve složce `game/`

## Logika hry
### Získání možných tahů
Možné tahy získáme tak, že v 2D poli reprezentující herní plochu projdeme každé
políčko a pokud je prázdné (je na něm nula) pokusíme se najít "anchory" neboli
opěrné kameny. Opěrné kameny jsou přesně ty, už existující kameny, z popisu
možných tahů. Konkrétně z kontrolovaného políčka prohledávám herní desku do
všech směrů a pokud po souvislé posloupnosti kamenů nepřítele narazím na nějaký
svůj, vím, že jsem našel opěrný bod a tedy je kontrolované políčko validní tah.
Důležité je i tak projít všechny další směry, protože kámen může mít více
opěrný bodů ve více směrech.

Možné tahy pro oba hráče udržuji jako seznam ve tvaru [None, seznam možných
tahů pro hráče 1, stejný seznam pro hráče -1] vyhledávání tahů pro specifického
hráče je tak velmi jednoduché. Opěrné body pro jednotlivé možné tahy udržuji ve
stejné struktuře a platí, že na pozici i v seznamu opěrných bodů (tedy seznamu
seznamů, protože opěrných bodů může být více) jsou opěrné body pro i-tý možný
tah se seznamu možných tahů.

### Hraní tahu
Funkce na hraní tahu dostává souřadnice políčka na které je záhodno umístit
aktuálního hráče. Pro tento tah si díky korespondenci popsané v minulém
odstavci najdeme opěrné body. Pro každý opěrný bod potom konvertujeme všechny
kameny mezi ním a novým tahem (hráči jsou reprezontováni jedničkou a minus
jedničkou takže stačí příslušné kameny vynásobit -1)

U toho je dobré udržovat si počet kamenů obou hráčů abychom dokázali určit
vítěze bez procházení celé herní plochy.

## Vykreslení hry 
K vykreslovnání používám knihovnu Pygame kterou pro kameny obaluje třída `Stone`.

Důležitou optimalizací je seznam `rects_to_change` do které se v průběhu
herního cyklu přidávají regiony které je nutno na obrazovce změnit. Nemusíme
tak každý snímek překreslovat celou obrazovku ale jen tu její část která to
vyžaduje.


# Monte-Carlo tree search

Metoda monte carlo použitá pro počítačového protivníka funguje na principu
opakovaného procházení stromu a odhadování kvality tahů na základě simulací a
jejich výsledků.

Konkrétně se jedná o kroky:
 - Select
 - Expand
 - Simulate
 - Back-propagate.
 Všechny tyto kroky poté spojíme do funkce `rollout`. Podrobnější popis následuje.


## Herní stav
Jednotlivé herní stavy reprezentujeme třídou `MTSNode` která dědí z třídy
`Board`. Kromě herní plochy si `MTSNode` musí pamatovat všechny své možné
následníky (ty už prozkoumané jako instanci stejné třídy, ty neznámé jako index
položeného kamene). Dále je klíčové si ukládat kolikrát jsme se z tohoto stavu
dostali k výhře hráče 1 a -1, tuto hodnotu upravuje metoda `back-propagate`.

## Select
Pro daný herní stav najde prvního (z pohledu hladin stromu) potomka který nemá
žádné své potomky. "Mít potomky" je zde myšleno jakože existuje jejich instance
třídy `MTSNode`. Pokud nějaký herní stav má už všechny své syny ve formě
`MTSNode` rozhodujeme se podle UCT.

### UCT 
UCT (Upper Confidence bound applied to Trees) je vzorec který se pokouší řešit
problém exploitation vs. exploration (do češtiny přeložitelný jako: když něco
funguje tak to neměň vs. dokud nezkusíš tak nevíš). Tento vzorec na základě
počtu navštívení daného vrcholu a jeho otce (n_i,N_i) a počtu výher pramenící z
tohoto stavu (w_i) určí jak moc dobrý následník je daný syn a tak jednoduše vybereme toho nejlepšího. 

Konkrétně se jedná o vzorec
w_i / n_i + c*(ln(N_i) / n_i )^1/2.

## Expand
Pro herní stav s ještě neprozkoumaným vrcholem vygeneruje jeho instanci `MTSNode` a vrátí ji.

## Simulate
Dohraje hru z daného vrcholu a vrátí jejího vítěze.

## Back-propagate
Vrací se po cestě vygenerované `select`em a do každého vrcholu na to správné
místo přidává hodnotu z `simulate`.

## Rollout
Jak už bylo naznačeno, jedná se o spojení všech předchozích funkcí. Pro daný
vrchol nejdřív najdeme jeho potomka s neprozkoumaným synem, toho rozšíříme. Z
nově přidaného vrcholu hru odsimulujeme až do konce a nakonec probubláme
výsledek simulace až zpátky ke kořeni.

## Jak táhne AI?
Jeden tah probíhá tak, že se ze současného herního stavu provede konstantní
počet `rollout`ů a nakonec se stejnou metodou UCT vybere nejlepší syn.

Kromě konstanty ovládající počet `rollout`ů je v souboru `ai/mts_constants.py`
také konstanta ovlivňující kolikrát se bude simulovat v rámci jednoho
`rollout`u. Tyto dvě konstanty dohromady udávají kvalitu protivníkovi hry a
také délku jeho tahů. 
