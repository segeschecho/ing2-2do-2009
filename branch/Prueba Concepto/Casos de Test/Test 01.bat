:: Test 01.bat
:: Primer caso de test
@echo off
del TR\*.tr
del EC\*.ec
echo **************************************************** 
echo Caso de Test 01
echo Descripcion :
echo    Existen 5 TR que envian cada 20 segundos y
echo    una se cae a los 45 segundos.
echo    Luego de esto 50 seg más tarde la TR se recupera
echo    y la EC lo reconoce!
echo **************************************************** 
::start Canal.py
::start RecepcionSegura.py
echo Levanto El Canal
start ..\Canal.py
echo Levanto La RecepcionSegura de la EC
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida
start ..\RecepcionSegura.py 40
:: Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida
echo Levanto las 5 TR
start ..\TR.py 20 4 1 45
start ..\TR.py 20 9 2 80000
start ..\TR.py 20 9 3 80000
start ..\TR.py 20 9 4 80000
start ..\TR.py 20 9 5 80000
Pause.py 45
echo Se cae TR 1
Pause.py 50
echo Se levanta TR 1
start ..\TR.py 20 3 1 80000
pause
echo on
