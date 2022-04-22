#!/bin/bash
set -eo pipefail
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
python -c "import lenstronomy"
pytest tests
pytest --cov=desclamp
exit 0
