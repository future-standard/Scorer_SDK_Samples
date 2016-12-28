#!/bin/sh

./killer.sh

python3 sdk_show1/scorer_show_sdk.py &
python3 sdk_show2/scorer_show_sdk.py &
python3 sdk_show3/scorer_show_sdk.py &
python3 sdk_show4/scorer_show_sdk.py &
