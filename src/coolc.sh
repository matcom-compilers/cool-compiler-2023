# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "IceBox: Turning COOL code into cooler results!"        #
echo "Copyright (c) 2019: Dario Fragas, Abraham González"    # TODO: líneas a los valores correctos

# Exec the compiler
exec python3 cool.py "$@"  
