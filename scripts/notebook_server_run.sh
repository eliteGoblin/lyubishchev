#!/bin/bash

set -euo pipefail

source .env/bin/activate
source .dotenv/myenv

jupyter notebook --no-browser