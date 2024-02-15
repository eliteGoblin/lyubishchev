#!/bin/bash

set -euo pipefail

# Define an array of pages
pages=(
    "http://127.0.0.1:8888/notebooks/time_report_notebook/SingleDay.ipynb" 
    "http://127.0.0.1:8888/notebooks/time_report_notebook/WeekReport.ipynb" 
    "http://127.0.0.1:8888/notebooks/time_report_notebook/MonthReport.ipynb"
)

# Iterate over the array and open each page
for page in "${pages[@]}"
do
#    /mnt/c/Windows/System32/cmd.exe /c start "$page" > /dev/null 2>&1
    xdg-open "$page" > /dev/null 2>&1
done