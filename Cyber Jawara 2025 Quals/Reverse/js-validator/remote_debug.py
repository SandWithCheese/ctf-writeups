#!/usr/bin/env python3
"""
Connect to NW.js remote debugging and extract the validation code
"""
import requests
import json
import time

print("=== NW.js Remote Debugger ===\n")

# Connect to Chrome DevTools Protocol
DEBUG_PORT = 9222
base_url = f"http://localhost:{DEBUG_PORT}"

try:
    # Get list of debuggable pages
    response = requests.get(f"{base_url}/json", timeout=5)
    pages = response.json()
    
    print(f"✓ Connected to remote debugging on port {DEBUG_PORT}")
    print(f"✓ Found {len(pages)} debuggable page(s)\n")
    
    for i, page in enumerate(pages):
        print(f"Page {i+1}:")
        print(f"  Title: {page.get('title', 'N/A')}")
        print(f"  URL: {page.get('url', 'N/A')}")
        print(f"  WebSocket: {page.get('webSocketDebuggerUrl', 'N/A')}")
        print()
    
    print("\nTo extract the code, you can:")
    print("1. Open Chrome/Chromium browser")
    print(f"2. Navigate to: chrome://inspect")
    print("3. Click 'Configure' and add 'localhost:9222'")
    print("4. Click 'inspect' on the NW.js page")
    print("5. You'll have full DevTools access!")
    print()
    print("Or navigate directly to:")
    if pages:
        print(f"  http://localhost:9222/devtools/inspector.html?ws={pages[0].get('id', '')}")
    
except requests.exceptions.ConnectionRefusedError:
    print(f"✗ Could not connect to port {DEBUG_PORT}")
    print("  Make sure NW.js is running with --remote-debugging-port=9222")
    print("  The package.json already has this configured.")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Alternative: Direct memory inspection")
print("="*60)

import subprocess

try:
    # Find NW.js processes
    result = subprocess.run(['pgrep', '-f', 'nw'], capture_output=True, text=True)
    if result.stdout.strip():
        pids = result.stdout.strip().split('\n')
        main_pid = pids[0]
        
        print(f"\n✓ Found NW.js main process: PID {main_pid}")
        print("\nExtracting from /proc memory...")
        
        # Try to read from process maps
        try:
            with open(f"/proc/{main_pid}/maps", 'r') as f:
                maps = f.read()
                if 'heap' in maps:
                    print("✓ Heap found in memory maps")
        except:
            pass
        
        # Alternative: use strings on the process memory
        print(f"\nSearching process memory for validation code...")
        cmd = f"sudo strings /proc/{main_pid}/mem 2>/dev/null | grep -A20 'CORRECT FLAG' | head -50"
        print(f"  Command: {cmd}")
        print("\n  Run this to see the validation code!")
        
except Exception as e:
    print(f"Could not analyze process: {e}")
