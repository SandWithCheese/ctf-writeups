#!/bin/bash
#
# auto-loop EXIF-SQLi flag harvester & submitter
# reruns the Python solver indefinitely with delay
#

SOLVER="./flag.py"   # path to the solver above
DELAY=300                      # seconds between runs
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MTYxMjY1NCwianRpIjoiZGYzY2FiNWMtNWI2Ny00OTRmLWFhMDYtM2I0OWE5N2ZjMDI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imtlc3Nva3Ugbm8gc2FpZ28gbm8gdGF0YWthaSIsIm5iZiI6MTc2MTYxMjY1NCwiY3NyZiI6IjJhNmI3Y2Q3LTMwMjMtNDA3Ni1hNmE4LWVmNmZkNThhMzdkNCIsImV4cCI6MTc2MTY5OTA1NH0.woNo3ovxraYYDbpxl0iRAql3djRCeKZZ13t2U8YXQ0M"                       # put your Bearer token here (optional)

echo "[*] Auto-loop started at $(date)"
echo "[*] Running $SOLVER every $DELAY seconds"
echo

while true; do
  echo "======================================="
  echo "[*] $(date): Starting new solver run..."
  echo "======================================="

  if [[ -n "$TOKEN" ]]; then
    python3 "$SOLVER" --workers 12 --token "$TOKEN"
  else
    python3 "$SOLVER" --workers 12 --no-submit
  fi

  ret=$?
  echo "[*] Solver exited with code $ret"
  echo "[*] Sleeping $DELAY seconds..."
  sleep "$DELAY"
done
