:: Test 02.bat
:: Segundo caso de test
@echo off
del BD\*.pu
del Resultados\*.ec
echo **************************************************** 
echo Test 02: Tres Estaciones Centrales se suscriben 
echo entre si, para intercambiar datos de sus modelos.
echo Cinco segundos más tarde se suscribe una nueva
echo Estacion central
echo **************************************************** 
echo Levanto las ECs.
:: Las ECs tienen dos parametros : id ec, dicc de otra id ec en a array de tipos de resultdos
start ..\EC.py  1 "{}"
echo Levantada EC 1...OK.
start ..\EC.py  2 "{\"1\":[\"TOTAL\"]}" 
echo Levantada EC 2...OK.
start ..\EC.py  3 "{\"1\":[\"TOTAL\"],\"2\":[\"PARCIAL\"]}"
echo Levantada EC 3...OK.
echo Se levantaron correctamente todas las ECs.
echo Se esperan 10 segundos...
Pause.py 10
echo Pasaron 10 segundos...
start ..\EC.py  4 "{\"3\":[\"PARCIAL\"],\"1\":[\"PARCIAL\", \"TOTAL\"]}"
echo Se levanto la EC 4...
pause
echo on