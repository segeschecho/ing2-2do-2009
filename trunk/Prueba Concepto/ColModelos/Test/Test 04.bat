:: Test 04.bat
:: Cuarto caso de test
@echo off
del BD\*.pu
del Resultados\*.ec
echo **************************************************** 
echo Test 02: Una estacion Central arranca, y diez segundos 
echo mas tarde se suscriben dos a ella.
echo **************************************************** 
echo Levanto las ECs.
:: Las ECs tienen dos parametros : id ec, dicc de otra id ec en a array de tipos de resultdos
start ..\EC.py  1 "{}"
echo Levantada EC 1...OK.
echo Se levantaron correctamente todas las ECs.
echo Se esperan 10 segundos...
Pause.py 10
echo Pasaron 10 segundos...
start ..\EC.py  2 "{\"1\":[\"TOTAL\"]}" 
echo Se levanto la EC 2...
start ..\EC.py  3 "{\"1\":[\"TOTAL\"],\"2\":[\"PARCIAL\"]}"
echo Se levanto la EC 3...
pause
echo on