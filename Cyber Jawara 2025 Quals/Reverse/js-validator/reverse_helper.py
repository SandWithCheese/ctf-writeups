#!/usr/bin/env python3
"""
Script to help reverse engineer the NW.js binary
This demonstrates how to programmatically inspect the running app
"""
import subprocess
import time
import json

print("=" * 60)
print("NW.js Binary Reverse Engineering Helper")
print("=" * 60)

print("""
INSTRUCTIONS:
============

1. The app should be running (npm start)
2. Open DevTools in the NW.js window (F12)
3. Go to Console tab
4. Try these commands:

STEP 1: Find new global variables
---------------------------------
Object.keys(window).filter(k => !k.startsWith('webkit') && !k.startsWith('chrome'))

STEP 2: Find the validation handler
------------------------------------
var btn = document.getElementById('validateBtn');
console.log('onclick:', btn.onclick);
console.log('listeners:', getEventListeners(btn));

STEP 3: Search for the validation code
---------------------------------------
// Press Ctrl+Shift+F in Sources tab
// Search for: "CORRECT FLAG"
// Search for: "sha256" or "SHA" or "hash"
// Search for: the checksum hash

STEP 4: Set breakpoint on validation
-------------------------------------
// In Sources tab, find the validation function
// Click line numbers to set breakpoints
// Enter a test flag and click Validate
// Step through the code (F10, F11)

STEP 5: Extract the code
-------------------------
// Once you find the validation function
// Right-click → "Copy function"
// Or use: 
console.log(btn.onclick.toString());

STEP 6: Bypass validation (quick win)
--------------------------------------
document.getElementById('validateBtn').onclick = function() {
    document.getElementById('result').textContent = 'CORRECT FLAG';
    document.getElementById('result').className = 'success';
    
    // Also log what the real validation would do
    var input = document.getElementById('flagInput').value;
    console.log('Flag:', input);
    console.log('SHA-256:', sha256(input)); // if sha256 function exists
};

""")

print("\n" + "=" * 60)
print("ALTERNATIVE: Use instrumented chall.js")
print("=" * 60)
print("""
1. Stop the current app (Ctrl+C on npm start)
2. Backup original: mv chall.js chall.js.bak
3. Use instrumented: cp chall_instrumented.js chall.js
4. Run again: npm start
5. Watch the console output - it will log EVERYTHING!
6. Restore after: mv chall.js.bak chall.js
""")

print("\n" + "=" * 60)
print("ADVANCED: Memory dump approach")
print("=" * 60)

try:
    # Find NW.js process
    result = subprocess.run(['pgrep', '-f', 'nw'], capture_output=True, text=True)
    if result.stdout.strip():
        pids = result.stdout.strip().split('\n')
        print(f"\n✓ Found NW.js process(es): {pids}")
        print(f"\nTo dump memory:")
        for pid in pids:
            print(f"  sudo gcore {pid}")
        print(f"\nThen search the dump:")
        print(f"  strings core.{pids[0]} | grep -A5 -B5 'CORRECT FLAG'")
        print(f"  strings core.{pids[0]} | grep -i 'function.*valid'")
    else:
        print("\n✗ No NW.js process found. Start the app first: npm start")
except Exception as e:
    print(f"Could not check for NW.js process: {e}")

print("\n" + "=" * 60)
print("QUICK TIPS")
print("=" * 60)
print("""
- The validation code MUST be in plain JavaScript when it runs
- DevTools can see everything that's loaded
- Use "Pause on exceptions" to catch errors
- Use "Event Listener Breakpoints" for DOMContentLoaded
- The bytecode is just an obfuscation layer - once loaded, it's JS!
""")

print("\n" + "=" * 60)
print("Ready to reverse! Open the app and DevTools now.")
print("=" * 60)
