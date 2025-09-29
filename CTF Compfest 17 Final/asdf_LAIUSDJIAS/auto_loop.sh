#!/bin/bash
#
# auto-loop web flag harvester & submitter
# reruns the Python solver indefinitely with delay
#

SOLVER="flag.py"   # path to your solver
DELAY=300                 # seconds between runs (tune if rate-limited)

echo "[*] Auto-loop started at $(date)"
echo "[*] Running $SOLVER every $DELAY seconds"
echo

while true; do
    echo "======================================="
    echo "[*] $(date): Starting new solver run..."
    echo "======================================="

    python3 "$SOLVER"

    ret=$?
    echo "[*] Solver exited with code $ret"
    echo "[*] Sleeping $DELAY seconds..."
    sleep "$DELAY"
done
