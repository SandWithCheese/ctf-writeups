#!/bin/bash

# A complete list of standard AWS regions as of 2025
REGIONS=(us-east-1 us-east-2 us-west-1 us-west-2 af-south-1 ap-east-1 ap-east-2 ap-south-1 ap-south-2 ap-northeast-1 ap-northeast-2 ap-northeast-3 ap-southeast-1 ap-southeast-2 ap-southeast-3 ap-southeast-4 ap-southeast-5 ap-southeast-7 ca-central-1 ca-west-1 eu-central-1 eu-central-2 eu-west-1 eu-west-2 eu-west-3 eu-south-1 eu-south-2 eu-north-1 il-central-1 mx-central-1 me-south-1 me-central-1 sa-east-1)

for region in "${REGIONS[@]}"; do
  echo "[-] Trying region: ${region}"
  # Run a simple, read-only command.
  aws cloudwatch describe-log-groups --region "${region}" 2>/dev/null
  # If the command is successful (exit code 0), we found the region.
  if [ $? -eq 0 ]; then
    echo -e "\n[+] SUCCESS! Found valid region: ${region}\n"
    exit 0
  fi
  sleep 1 # Respect the 1 req/sec limit
done

echo -e "\n[-] FAILED: No valid region found in the list."
