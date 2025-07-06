#!/bin/bash

set -euo pipefail

# Define an array of pages
pages=(
    "http://127.0.0.1:8888/notebooks/time_report_notebook/SingleDay.ipynb" 
    "http://127.0.0.1:8888/notebooks/time_report_notebook/WeekReport.ipynb" 
    "http://127.0.0.1:8888/notebooks/time_report_notebook/MonthReport.ipynb"
)

# Function to open URLs in the default browser
open_in_browser() {
    local url="$1"
    # Detect the OS and use the appropriate command
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux/Ubuntu
        xdg-open "$url" > /dev/null 2>&1
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$url" > /dev/null 2>&1
    else
        echo "Unsupported OS: $OSTYPE"
        exit 1
    fi
}

# Iterate over the array and open each page
for page in "${pages[@]}"
do
    open_in_browser "$page"
done

