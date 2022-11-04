echo off
echo Ve stejne slozce jako je tento skript musi byt soubor s tapetou 'wallpaper.jpg'.
echo Zadejte prihlasovaci udaje do bakalaru. Je to jen jednorazove a nikde se neukladaji.
echo Pokud se vse povede, vyskoci systemova notifikace a zmeni se tapeta.
echo.

set /p un="Jmeno: "
set /p ps="Heslo: "
pyvenv\Scripts\python.exe source\main.py %un% %ps%
echo Program spusten. Bezi na pozadi.
pause
