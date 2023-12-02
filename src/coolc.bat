@echo off
REM Incluya aquí las instrucciones necesarias para ejecutar su compilador

set INPUT_FILE=%1
set OUTPUT_FILE=%~n1mips

REM Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo Cool-Compiler-2020: v1.0
echo Copyright (c) 2019: Karlos Alejandro Alfonso Rodríguez, Laura Victoria Riera Pérez, Kevin Talavera Díaz

REM Llamar al compilador
REM echo Compiling %INPUT_FILE% into %OUTPUT_FILE%

REM check python3 -m main -h for help
python -m main %INPUT_FILE%