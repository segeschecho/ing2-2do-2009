:: Simulacion.bat
:: Crea los procesos necesarios para
:: la prueba de concepto
@ECHO OFF
del TR\*.tr
del TR\*.ec
del EC\*.tr
del EC\*.ec
TR.py 1
TR.py 2
ECHO.
pause

