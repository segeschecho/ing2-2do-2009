:: Simulacion.bat
:: Crea los procesos necesarios para
:: la prueba de concepto
del EC\.tr
del TR\.ec
del TR\.tr
del EC\.ec
start Canal.py
start RecepcionSegura.py
start TR.py 2 2 1
start TR.py 3 1 2
