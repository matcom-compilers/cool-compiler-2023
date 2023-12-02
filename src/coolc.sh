# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool Compiler 2023: v1.0"
echo "Copyright (c) 2019: Karlos Alejandro Alfonso Rodríguez, Laura Victoria Riera Pérez, Kevin Talavera Díaz" 

# Llamar al compilador
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python3 -m main $INPUT_FILE
