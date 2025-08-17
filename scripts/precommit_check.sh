#!/bin/bash

set -euo pipefail

source .venv/bin/activate

jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace time_report_notebook/*.ipynb

git add . && ./scripts/ci/ci

