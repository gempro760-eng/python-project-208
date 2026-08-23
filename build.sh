#!/usr/bin/env bash

set -e

# descargamos uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
# comandos de funcionamiento
make install && make collectstatic && make migrate