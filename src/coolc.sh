
echo "Cool 1.0.0"
echo "Copyright (c) 2023: Lauren Guerra, Dennis Fiallo"

INPUT_FILE=$1
if [ -z "$1" ]; then
    echo -e "\nError: No input provided" >&2
    exit 1
fi
OUTPUT_FILE=${INPUT_FILE:0: -2}mips


python run.py $INPUT_FILE $OUTPUT_FILE