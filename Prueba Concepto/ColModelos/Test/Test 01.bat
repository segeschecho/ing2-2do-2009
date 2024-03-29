:: Test 01.bat
:: Primer caso de test
@echo off
del BD\*.pu
del Resultados\*.ec
echo **************************************************** 
echo Test 01: Cuatro Estaciones Centrales se suscriben 
echo entre si, para intercambiar datos de sus modelos
echo **************************************************** 
echo Levanto las ECs.
:: Las ECs tienen dos parametros : id ec, dicc de otra id ec en a array de tipos de resultdos
start ..\EC.py  1 "{}"
echo Levantada EC 1...OK.
start ..\EC.py  2 "{\"1\":[\"TOTAL\"]}" 
echo Levantada EC 2...OK.
start ..\EC.py  3 "{\"1\":[\"TOTAL\"],\"2\":[\"PARCIAL\"]}"
echo Levantada EC 3...OK.
start ..\EC.py  4 "{\"3\":[\"PARCIAL\"],\"1\":[\"PARCIAL\", \"TOTAL\"]}"
echo Levantada EC 4...OK.
echo Se levantaron correctamente todas las ECs.
pause
echo on
