#!/bin/bash
set -eo pipefail
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
python -c "import lenstronomy"
python -m pip install .
pytest tests
pytest --cov=desclamp
exit 0
