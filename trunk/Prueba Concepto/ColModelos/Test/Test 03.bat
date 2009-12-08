:: Test 03.bat
:: Tercer caso de test
@echo off
del BD\*.pu
del Resultados\*.ec
echo **************************************************** 
echo Test 03: Tres Estaciones Centrales no se suscriben 
echo a ninguna por lo cual no se debe pasar ningun resultado.
echo **************************************************** 
echo Levanto las ECs.
:: Las ECs tienen dos parametros : id ec, dicc de otra id ec en a array de tipos de resultdos
start ..\EC.py  1 "{}"
echo Levantada EC 1...OK.
start ..\EC.py  2 "{}" 
echo Levantada EC 2...OK.
start ..\EC.py  3 "{}"
echo Levantada EC 3...OK.
echo Se levantaron correctamente todas las ECs.
pause
echo on