:: Test 03.bat
:: Tercer caso de test
@echo off
del TR\*.tr
del EC\*.ec
echo **************************************************** 
echo Caso de Test 03
echo Descripcion :
echo    Existen 5 TR que envian cada 20 segundos y
echo    ninguna se cae, pero la EC toma 10 seg como 
echo    tiempo para asumir que se caen las TR, esto
echo    va a generar que se asuma que se cayo la TR
echo    aunque en ralidad no paso.
echo    Cada TR se levanta con 3 seg de diferencia del
echo    la anterior.
echo **************************************************** 
::start Canal.py
::start RecepcionSegura.py
echo Levanto El Canal
start ..\Canal.py
echo Levanto La RecepcionSegura de la EC
:: La RecepcionSegura tiene un parametro : tiempo para detectar caida
start ..\RecepcionSegura.py 10
:: Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida
echo Levanto las 5 TR
start ..\TR.py 20 15 1 80000
Pause.py 3
start ..\TR.py 20 15 2 80000
Pause.py 3
start ..\TR.py 20 15 3 80000
Pause.py 3
start ..\TR.py 20 15 4 80000
Pause.py 3
start ..\TR.py 20 15 5 80000
pause
echo on
