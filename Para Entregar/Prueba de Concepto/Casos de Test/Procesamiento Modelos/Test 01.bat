:: Test 01.bat
:: Primer caso de test
@echo off
echo **************************************************** 
echo Caso de Test 01 (Modulo Procsamiento)
echo Descripcion :
echo    Se utilizan las reglas1.py y ademas se le pasa
echo    el archivo de datos datos1.py.
echo **************************************************** 
python ..\..\Modelos.py ..\..\reglas1.py ..\..\datos1.py
pause
echo on