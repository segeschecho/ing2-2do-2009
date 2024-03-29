:: Test 08.bat
:: Primer caso de test
@echo off
del TR\*.tr
del EC\*.ec
del BDESTADO\*.tr
del BDESTADO\*.pu
echo **************************************************** 
echo Caso de Test 08
echo Descripcion :
echo    Existen 5 TR que envian cada 20 segundos
echo    y 2 EC que se suscriben a varios sensores
echo    de cada tr.
echo    Las 2 ec comparten la suscripcion a la TR 3.
echo    Esta se cae a los 42 segundos.
echo    y luego vuelve, sabiendo a que ECs enviar su info.
echo **************************************************** 
::start Canal.py
::start RecepcionSegura.py
echo Levanto El Canal
start ..\Canal.py
:: Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida
echo Levanto las TRs
start ..\TR.py 20 3 1 80000 
start ..\TR.py 20 2 2 80000
start ..\TR.py 20 2 3 20
start ..\TR.py 20 9 4 80000
start ..\TR.py 20 9 5 80000

echo Levanto La RecepcionSegura de la EC
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida, id ec, dicc de idTR a array de sensores
Pause.py 5
start ..\EC.py 15 11 "{\"1\":[\"Presion\",\"Temperatura\"],\"2\":[\"Temperatura\"], \"3\":[\"Temperatura\"]}" "{}"
start ..\EC.py 15 12 "{\"3\":[\"Humedad\"], \"4\":[\"Presion\", \"Humedad\"], \"5\":[\"Presion\", \"Humedad\"]}" "{}"
Pause.py 30
echo Se cae TR 3
Pause.py 50
echo Se levanta TR 3
start ..\TR.py 20 2 3 80000
pause
echo on

