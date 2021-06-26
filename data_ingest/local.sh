#!/bin/bash

set -eu

VENV_PATH=.venv/
VENV_PYTHON=${VENV_PATH}bin/python
VENV_PIP=${VENV_PATH}bin/pip

if [[ -f ${VENV_PYTHON} ]]; then
    echo "Re-using existing virtualenv at: ${VENV_PATH} and assuming it's up to date."
    echo "If you see errors try 'rm -rf ${VENV_PATH}' and re-run this script."
else
    echo "Creating virtual env at: ${VENV_PATH}..."
    python3 -m venv ${VENV_PATH}
    ${VENV_PIP} install -r ./requirements.txt
fi

${VENV_PYTHON} -m test $@