#!/bin/bash

LOG_FILE="organizer.log"

# Create the archive folder if it does not exist
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Stop if there is no grades.csv to archive
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv not found."
    exit 1
fi

# Build the timestamp and the new filename
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

# Rename and move the file into archive
mv grades.csv "archive/${ARCHIVED_NAME}"

# Create a new empty grades.csv
touch grades.csv

# Append the details to the log
echo "[${TIMESTAMP}] Original: grades.csv | Archived: archive/${ARCHIVED_NAME}" >> "$LOG_FILE"

echo "Archived to archive/${ARCHIVED_NAME}. New empty grades.csv created."