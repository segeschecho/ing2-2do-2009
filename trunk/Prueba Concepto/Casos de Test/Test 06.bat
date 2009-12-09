:: Test 06.bat
:: Primer caso de test
@echo off
del TR\*.tr
del EC\*.ec
del BDESTADO\*.tr
del BDESTADO\*.pu
echo **************************************************** 
echo Caso de Test 06
echo Descripcion :
echo    Existen 3 TR que envian cada 20 segundos
echo    y la EC 12 se suscriben a varios sensores de la
echo    EC 11.
echo **************************************************** 
::start Canal.py
::start RecepcionSegura.py
echo Levanto El Canal
start ..\Canal.py
:: Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida
echo Levanto las TRs
start ..\TR.py 20 3 1 80000 
start ..\TR.py 20 2 2 80000
start ..\TR.py 20 2 3 80000
:: start ..\TR.py 20 9 4 80000
:: start ..\TR.py 20 9 5 80000
echo Levanto La RecepcionSegura de la EC
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida, id ec, dicc de idTR a array de sensores
Pause.py 5
start ..\EC.py 40 11 "{\"1\":[\"Presion\",\"Temperatura\"],\"2\":[\"Temperatura\"]}" "{}"
start ..\EC.py 40 12 "{\"3\":[\"Humedad\"]}" "{\"11\":{\"1\":[\"Presion\"],\"2\":[\"Temperatura\"]}}"
:: Pause.py 45
:: echo Se cae TR 1
:: Pause.py 50
:: echo Se levanta TR 1
:: start ..\TR.py 20 3 1 80000
pause
echo on

