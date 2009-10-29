:: Test 02.bat
:: Segundo caso de test
@echo off
del TR\*.tr
del EC\*.ec
echo **************************************************** 
echo Caso de Test 02
echo Descripcion :
echo    Existen 5 TR que envian cada 20 segundos y
echo    ninguna se cae.
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
start ..\TR.py 20 15 1 80000
start ..\TR.py 20 15 2 80000
start ..\TR.py 20 15 3 80000
start ..\TR.py 20 15 4 80000
start ..\TR.py 20 15 5 80000
pause
echo on
