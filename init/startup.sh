#!/bin/bash

VIRTENV_ROOT=/root/.virtualenv/pi_controls
PICONTROL_ROOT=/usr/local/pi_control/R.Pi_Controls

source $VIRTENV_ROOT/bin/activate
$PICONTROL_ROOT/pi_controls.py
