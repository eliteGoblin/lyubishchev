#!/bin/bash

set -euo pipefail

source .venv/bin/activate
source .dotenv/myenv

jupyter notebook --no-browser
