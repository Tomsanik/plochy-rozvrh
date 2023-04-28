# Plochý rozvrh
Program využívající API Bakalářů pro snazší přístup k aktuálnímu rozvrhu. Určeno zejména pro učitele pro využití na pracovních počítačích.

## Popis
Dokáže stáhnout váš aktuální rozvrh a v pěkné podobě zobrazit v rohu tapety plochy.
Výhodou takto umístěného rozvrhu je to, že ho má učitel neustále po ruce bez toho, aby musel otevírat aplikaci Bakaláři nebo záložku v prohlížeči (která se stejně časem ztratí mezi ostatními nebo odhlásí). Pozor! Nejedná se o widget. Rozvrh je součásti tapety, takže nikde nepřekáží.

## Obsah dokumentace
* [Co program umí](#co-program-umí)
* [Co program neumí](#co-neumí)
* [Instalace](#instalace)
* [Poznámky k instalaci](#poznámky-k-instalaci)
* [Aktualizace na novější verzi](#aktualizace-na-novější-verzi)
* [První spuštění](#první-spuštění)

## Co program umí
- Rozvrh se aktualizuje ráno v 7:30 a poté při každém zvonění na přestávku (na konci hodiny).
- Kdykoli lze vynutit okamžitou obnovu.
- Za běhu se minimalizuje do ikonky v oznamovací oblasti lišty, takže nikde nepřekáží otevřené okno.
- Vzhled rozvrhu na ploše jde změnit úpravou CSS souboru.
- Funguje pro všechny školy provozující systém Bakaláři.
- Přehledně zobrazuje změny v rozvrhu včetně odpadlých hodin, změn učebny apod.
- Lze si zvolit, jakou tapetu chcete použít.
- Umožňuje zobrazit jakýkoli týden v budoucnu i v minulosti a zároveň se snadno vrátit do aktuálního týdne.
- Pro aktuální týden zvýrazní nadcházející hodinu, aby učitel snadno našel, koho bude zrovna učit a kde.
- Vše funguje stejně i pro žáky (toto tvrzení je třeba ověřit praxí).
- Program se nespouští automaticky, je třeba ho po zapnutí PC spustit a přihlásit se.
- Po prvním přihlášení uloží školu a přihlašovací jméno, abyste ho už nemuseli zadávat. Poté je tedy potřeba zadat pouze heslo.
- Program komunikuje pouze s vámi vybraným serverem Bakalářů. Žádná data se nikam jinam neodesílají.
- Plně free open source, tak jak to má být:).

## Co neumí:
- Spoustu věcí, ale nejvíce iritující je nemožnost zobrazení dohledů, suplovacích pohotovostí a zámečků (poslední hodina ve třídě). Data bohužel nejsou získatelná přes API Bakalářů.

## Instalace
- Pro funkčnost je bohužel potřeba mít **nainstalovaný prohlížeč [Google Chrome](https://www.google.com/intl/cs/chrome/)**. Je to proto, že se jeho headless API používá na získání obrázku rozvrhu, který je vytvořen pomocí HTML+CSS.
- Je potřeba **[nainstalovat Python3](https://www.python.org/downloads/)**. Verze 3.10 a vyšší určitě funguje, na nižších jsem to nezkoušel, ale nemusel by to být problém.
- **Stáhněte soubory z GitHubu** a rozbalte do složky, kde bude program přebývat. Doporučuji např. domovskou složku, ale i roh plochy postačí.
- **Spusťte skript *get_venv.bat*.** Tento skript vytvoří lokální virtuální prostředí Python ve složce s programem a stáhne do něj potřebné závislosti (soubor requirements.txt). Nechte skript doběhnout (cca 1 minutu) a až budete vyzváni, stiskněte libovolnou klávesu. Tím vznikne adresář *venv*.
- Vše je připravené, můžete **program spustit pomocí skriptu *RUN.bat*.**

## Poznámky k instalaci
- Pro budoucí pohodlí doporučuji vytvořit zástupce *RUN.bat* na ploše.
- Oba skripty jsou velice jednoduché a nedělají nic nekalého. Doporučuji jejich kontrolu v textovém editoru.

## Aktualizace na novější verzi
- Program neobsahuje žádného automatického aktualizátora, který by běžel na pozadí.
- Smažte celou složku s programem, kterou máte v PC. Pozor na tapetu, pokud tam máte svoji.
- Proveďte instalaci znovu počínaje třetím krokem (stažení z GitHubu).

## První spuštění
- Vyberte město a školu (nebojte, stačí pouze jednou).
- Zadejte přihlašovací jméno a heslo do Bakalářů (stejné jako do webového rozhraní).
- Klikněte na Přihlásit se.
- Políčka zešednou a objeví se tlačítko Minimalizovat. Jeho stisknutím se program přesune do oznamovací lišty. Stejný efekt má i křížek v rohu okna.
- Město, škola a uživatelské jméno se uloží do adresáře s programem. Při dalším přihlášení bude potřeba zadat pouze heslo.

## Ukončení programu:
- Pro ukončení programu je potřeba se odhlásit kliknutím na tlačítko Odhlásit.
- Program ukončíte tlačítkem Ukončit nebo křížkem v rohu okna.

## Tipy:
- Na plochu se ve Windows dá snadno dostat kliknutím do úplného pravého konce lišty (pravý dolní roh obrazovky).
- Opětovným kliknutím se obnoví poloha oken.
- Ve složce source je celý zdrojový kód. Program je obyčejný Python. Feel free to browse and modify.
- V základní složce programu je soubor *wallpaper.png*. Ten můžete nahradit libovolnou jinou tapetou ve fomátu *PNG*, jen ji pojmenujte opět *wallpaper.png*. Program zvládne libovolné rozlišení tapety s tím, že si rozvrh naškáluje na danou velikost na obrazovce.

## Testovací provoz:
- Program byl testován ponejvíce autorem a úzkým okruhem kolegů.
- Je v podstatě jisté, že rozmanitost škol, počítačů a uživatelů napříč školstvím objeví nejednu chybu.
- Při objevení jakékoliv závady či nefunkčnosti prosím nahlásit založením **Issue na Githubu**. Časem sem přidám i mail dedikovaný pro tento účel.
- Za screenshoty s problémy budu rád.

## Návod na debugging (mírně pokročilí):
- Když se program chová nestandardně (neaktualizuje rozvrh, nejde přihlásit, nejde spustit,...), je možné zjistit, co se děje pohledem do hlubin výpisu programu.
- Je třeba, aby se program nespouštěl pomocí windowless Pythonu, ale normálního.
- Ve skriptu *RUN.bat* upravte v cestě k Pythonu slovo
…/python**w**.exe… na slovo
…/python.exe…
- Po opětovném spuštění se k programu spustí i konzole, kde jsou vidět jeho výpisy. S těmi možná budete schopni problém vyřešit, případně ho přiložte k Issue pro snazší opravu.
- Pokud byste narazili na problém, který se vám povedlo spravit, dejte prosím vědět.
