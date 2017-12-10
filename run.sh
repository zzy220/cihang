CURDIR=`pwd`
export PYTHONPATH=${PYTHONPATH}:${CURDIR}
WORKDIR="${CURDIR}/workdir"
echo "WORKDIR="${WORKDIR}
python3 -m onboardsvr ${WORKDIR}
