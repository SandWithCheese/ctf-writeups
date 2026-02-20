#!/bin/bash
# Quick script to try the instrumented approach

echo "=== NW.js Binary Reverser ==="
echo

# Check if npm start is running
if pgrep -f "npm start" > /dev/null; then
    echo "✓ NW.js app is running"
    echo "  To see the app with DevTools:"
    echo "  1. Switch to the NW.js window"
    echo "  2. Press F12 to open DevTools"
    echo "  3. Go to Console tab"
    echo "  4. Try the commands from reverse_helper.py"
    echo
else
    echo "✗ NW.js app not running"
    echo "  Starting it now..."
    npm start &
    sleep 3
fi

echo
echo "=== METHOD 1: Use Instrumented chall.js ==="
echo

if [ ! -f "chall.js.bak" ]; then
    echo "Creating backup..."
    cp chall.js chall.js.bak
    echo "✓ Backed up chall.js → chall.js.bak"
fi

echo
echo "Do you want to use the instrumented version? (y/n)"
echo "(This will show all function calls and variables in console)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Copying instrumented version..."
    cp chall_instrumented.js chall.js
    echo "✓ Now using chall_instrumented.js"
    echo
    echo "Restarting app..."
    pkill -f "npm start"
    sleep 1
    npm start &
    echo
    echo "✓ App restarted with instrumentation!"
    echo "  Open DevTools (F12) and watch the console"
    echo
    echo "To restore original:"
    echo "  mv chall.js.bak chall.js"
else
    echo "Keeping original chall.js"
fi

echo
echo "=== METHOD 2: Memory Dump (Advanced) ==="
echo

# Find main NW.js process (usually the one with lowest PID)
main_pid=$(pgrep -f "nw" | head -1)

if [ -n "$main_pid" ]; then
    echo "Main NW.js PID: $main_pid"
    echo
    echo "To dump and analyze memory:"
    echo "  sudo gcore $main_pid"
    echo "  strings core.$main_pid | grep -C10 'CORRECT FLAG' > extracted.txt"
    echo "  cat extracted.txt"
fi

echo
echo "=== METHOD 3: Source Code Search (If DevTools is open) ==="
echo

cat << 'EOF'
In DevTools Console, paste this:

// Find all functions
for (let key in window) {
    if (typeof window[key] === 'function' && !key.startsWith('webkit')) {
        console.log('FUNCTION:', key);
        if (key.includes('valid') || key.includes('check') || key.includes('hash')) {
            console.log(window[key].toString());
        }
    }
}

// Or use this to dump everything
JSON.stringify(Object.keys(window), null, 2)
EOF

echo
echo "=== Ready! ==="
