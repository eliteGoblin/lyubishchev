#!/bin/bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace time_report_notebook/*.ipynb
git add . && ./local.sh