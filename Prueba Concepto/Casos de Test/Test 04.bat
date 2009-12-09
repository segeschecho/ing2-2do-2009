:: Test 01.bat
:: Primer caso de test
@echo off
del TR\*.tr
del EC\*.ec
del BDESTADO\*.tr
del BDESTADO\*.pu
echo **************************************************** 
echo Caso de Test 04
echo Descripcion :
echo    Existen 3 TR que envian cada 20 segundos
echo    Se corren 2 ECs y se suscriben a los mismos
echo **************************************************** 
::start Canal.py
::start RecepcionSegura.py
echo Levanto El Canal
start ..\Canal.py
:: Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida
echo Levanto las TRs
start ..\TR.py 20 3 1 80000 
start ..\TR.py 20 2 2 80000
start ..\TR.py 20 1 3 80000
:: start ..\TR.py 20 9 4 80000
:: start ..\TR.py 20 9 5 80000

Pause.py 10

echo Levanto La RecepcionSegura de la EC
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida, id ec, dicc de idTR a array de sensores
start ..\EC.py 40 11 "{\"1\":[\"Temperatura\"],\"2\":[\"Presion\"]}" "{}"

echo Levanto La RecepcionSegura de la EC
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida, id ec, dicc de idTR a array de sensores
start ..\EC.py 40 12 "{\"1\":[\"Temperatura\"], \"2\":[\"Humedad\"], \"3\":[\"Presion\", \"Temperatura\"]}" "{}"

#Pause.py 45
#echo Se cae TR 1
#Pause.py 50
#echo Se levanta TR 1
#start ..\TR.py 20 3 1 80000
pause
echo on
