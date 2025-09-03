#!/bin/bash

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_file> [output_file]"
    echo "Example: $0 ips.txt ping_results.csv"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-ping_results.csv}"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found!"
    exit 1
fi

# Create CSV header
echo "IP address,Pingable" > "$OUTPUT_FILE"

# Read each IP from the file
while IFS= read -r ip; do
    # Skip empty lines and comments
    if [[ -z "$ip" || "$ip" =~ ^# ]]; then
        continue
    fi

    # Remove any whitespace
    ip=$(echo "$ip" | xargs)

    # Ping the IP with 1 packet (adjust for different OS)
    # For Linux (uses -c and -W)
    if ping -c 1 -W 2 "$ip" > /dev/null 2>&1; then
        echo "$ip,Yes" >> "$OUTPUT_FILE"
    else
        echo "$ip,No" >> "$OUTPUT_FILE"
    fi

    # Alternative for macOS (uses -c and -t)
    # if ping -c 1 -t 2 "$ip" > /dev/null 2>&1; then
    #     echo "$ip,Yes" >> "$OUTPUT_FILE"
    # else
    #     echo "$ip,No" >> "$OUTPUT_FILE"
    # fi

done < "$INPUT_FILE"

echo "Ping results saved to: $OUTPUT_FILE"
