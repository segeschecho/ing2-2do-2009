# test1.sh
# Primer caso de test
rm TR\*.tr
rm EC\*.ec
echo **************************************************** 
echo Caso de Test 01
echo **************************************************** 

echo Levanto El Canal
gnome-terminal -e "python ../Canal.py" &

# Las TR's tienen 4 parametros : intervalo, cantidad , Id TR, tiempo vida

gnome-terminal -e "python ../TR.py 20 4 1 80000" &
gnome-terminal -e "python ../TR.py 20 9 2 80000" &

echo Levanto La RecepcionSegura de la EC
# La RecepcionSegura tiene un parametro : tiempo para detectar caida, id ec, dicc de idTR a array de sensores

gnome-terminal -e "python ../RecepcionSegura.py 40 1 '{\"1\":[\"Temperatura\"],\"2\":[\"Presion\"]}'" &


