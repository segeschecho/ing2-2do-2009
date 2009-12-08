:: Test 01.bat
:: Primer caso de test
@echo off
del BD\*.pu
del Resultados\*.ec
echo **************************************************** 
echo Prueba 01
echo **************************************************** 
::start Canal.py
::start RecepcionSegura.py
::echo Levanto El Canal
::start ..\Canal.py
:: Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida
::echo Levanto las TRs
::start ..\TR.py 20 4 1 80000 
::start ..\TR.py 20 9 2 80000
:: start ..\TR.py 20 9 3 80000
:: start ..\TR.py 20 9 4 80000
:: start ..\TR.py 20 9 5 80000
echo Levanto las ECs
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida, id ec, dicc de idTR a array de sensores
start ..\EC.py  1 "{}"
start ..\EC.py  2 "{\"1\":[\"TOTAL\"]}" 
start ..\EC.py  3 "{\"1\":[\"TOTAL\"],\"2\":[\"PARCIAL\"]}"
start ..\EC.py  4 "{\"3\":[\"PARCIAL\"],\"1\":[\"PARCIAL\", \"TOTAL\"]}"
:: Pause.py 45
:: echo Se cae TR 1
:: Pause.py 50
:: echo Se levanta TR 1
:: start ..\TR.py 20 3 1 80000
pause
echo on
