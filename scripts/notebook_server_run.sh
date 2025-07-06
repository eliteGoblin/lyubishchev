#!/bin/bash

export HTTPS_PROXY=http://df.proxy.prod.mte.westpac.com.au:8080
export HTTP_PROXY=http://df.proxy.prod.mte.westpac.com.au:8080

set -euo pipefail

source .env/bin/activate
source .dotenv/myenv

jupyter notebook --no-browser
