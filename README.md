# Plochý rozvrh
Program pracující s Bakaláři. Po přihlášení stáhne aktuální rozvrh a integruje jej v originálním formátu do tapety.
Program běží v pozadí a aktualizuje rozvrh na konci každé vyučovací hodiny (začátek vyučování v 8:00).
První aktualizace dne je v 7:30, poté na konci každé hodiny.
Rozvrh je na ploše snadno dustupný, stále aktuální a snadno modifikovatelný pomocí CSS souboru.

Funkce:
1) Po spuštění požaduje přihlášení. Údaje se nikde neukládají a použijí se pouze jednou. Další komunikace s bakaláři probíhá pomocí access tokenu.
2) Program běží na pozadí, nepřekáží na liště a nevytěžuje systémové zdroje.
3) První aktualizace je každý den v 7:30. Poté na konci každé vyučovací hodiny (časy jsou editovatelné ve zdrojovém kódu main.py).
4) Zvýrazňuje aktuální hodinu (hodinu následující po zrovna započaté přestávce).
5) Rozvrh se integruje do tapety přiložené k programu. Je možné výchozí tapetu nahradit jinou.
6) Nejlépe funguje na monitoru s FullHD rozlišení (1920x1080), ale není to podmínkou. Neměl by být problém s žádným standardním rozlišením, pokud bude použita správná tapeta.
7) Formát rozvrhu lze měnit v CSS souboru ve složce source. Obrázek rozvrhu je screenshot html souboru, který je sestaven skriptem (soubor get_html.py).
8) Program se nespouští sám po startu. Je možné udělat si zástupce skriptu RUN.bat na plochu nebo přidat skript do Po spuštění systému.
9) Tapetu ve Windows lze snadno zobrazit posunutím kurzoru do pravého spodního rohu obrazovky. Není potřeba žádné z oken minimalizovat na lištu.

Návod na použití:
1) Pro fungování programu je třeba mít nainstalovaný Python ve verzi alespoň 3.10
2) Spuštěním skriptu get-venv.bat se vytvoří virtuální prostředí Pythonu pro tento projekt ve složce s programem (pyvenv). Dále se prostředí naplní potřebnými balíky. Pro tento krok je třeba mít připojení k internetu. Je potřeba počkat na dokončení, kdy bude zobrazena výzva ke stisku klávesy.
3) Pokud dosud vše proběhlo bez problému, měl by jít spustit skritp RUN.bat. Ten se jednorázově zeptá na přihlašovací údaje do Bakalářů. Ty slouží ke staženi přihlašovacích tokenů, nikam se neukládají a odesílají se pouze šifrovaně na servery Bakalářů. POZOR, PŘI ZADÁVÁNÍ JE JMÉNO I HESLO VIDITELNÉ.
4) Po zadání by se měl bez chyby spustit Python na pozadí a současné okno by mělo vyzvat k uzavření stiskem klávesy.
5) Během několika sekund by mělo prvně dojít k sestavení tapety.
6) Při každém obnovení vyskočí na pár sekund notifikace s upozorněním, že k němu došlo, a za jak dlouho probehe příště.

Při odhalení chyby založte Issue zde v GitHubu.
