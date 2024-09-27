#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <namespace> <podname-substring>"
    exit 1
fi

NAMESPACE="$1"
PODNAME_SUBSTRING="$2"
OUTPUT_FILE="top_pods.csv"

# Write CSV header
echo "TIMESTAMP,NAME,CPU(cores),MEMORY(bytes)" > $OUTPUT_FILE

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Get the top pods information, filter by name substring, and remove units
    TOP_PODS=$(kubectl top pods -n $NAMESPACE --no-headers | grep "$PODNAME_SUBSTRING" | awk -v ts="$TIMESTAMP" '{gsub(/m/,"",$2); gsub(/Mi/,"",$3); print ts","$1","$2","$3}')
    
    # Append to the CSV file
    echo "$TOP_PODS" >> $OUTPUT_FILE
    
    # Output to the console
    echo "$TOP_PODS"
    
    sleep 30
done
