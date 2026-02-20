# How to Reverse Engineer the NW.js Binary

## Why Brute Force is Bad

The Base64 message in the binary is a **RED HERRING**:
```
__congrats_AI_you_found_this_to_get_the_flag_you_can_easily_brute_flag...
```

This is intentionally misleading to waste your time. The proper approach is to **decompile or dynamically analyze** the V8 bytecode.

---

## Method 1: Dynamic Analysis (★ RECOMMENDED - Easiest)

This is the most reliable method since the code must execute in plain JavaScript at runtime.

### Steps:

1. **Run the application:**
   ```bash
   npm start
   ```

2. **Open DevTools:**
   - Press `F12` or `Ctrl+Shift+I`
   - Or right-click → "Inspect Element"

3. **Enable debugging BEFORE the binary loads:**
   
   **Option A: Modify `chall.js` to add debugger**
   ```javascript
   debugger;  // Add this line
   nw.Window.get().evalNWBin(null, 'chall.bin');
   ```

   **Option B: Set event listener breakpoint**
   - In DevTools → Sources tab
   - Event Listener Breakpoints → DOM Mutation → DOMContentLoaded
   - Reload the page

4. **Inspect the executed code:**
   - Once the code loads, you can:
     - View all global variables in Console
     - Set breakpoints on the validation function
     - Modify the validation logic in memory
     - Inspect the actual comparison happening

5. **Find the validation function:**
   ```javascript
   // In the Console, try:
   console.log(window);
   
   // Look for validation-related functions
   // Typically attached to the validateBtn click handler
   
   // You can also override the validation:
   document.getElementById('validateBtn').onclick = function() {
       var flag = document.getElementById('flagInput').value;
       console.log("Flag input:", flag);
       // Inspect what happens next
   };
   ```

6. **Extract the actual validation logic:**
   - The binary will be executed as JavaScript
   - Use the "Sources" tab to view the actual running code
   - Look for hash computations, comparisons, etc.

---

## Method 2: Using V8 Bytecode Decompiler Tools

### Option A: nwjs-decompiler (if available)

```bash
# Search for nwjs decompiler tools
npm search nwjs-decompiler
# or
pip search nwjs
```

### Option B: View8 (For V8 Snapshot Files)

**Note:** This tool is designed for `.jsc` files, but might work with `.bin` files.

```bash
# Install View8
git clone https://github.com/Check-Point-Research/View8
cd View8

# Follow the installation instructions
# Then try:
python view8.py ../chall.bin -o decompiled.txt
```

### Option C: Ghidra with ghidra_nodejs Plugin

1. **Install Ghidra:**
   - Download from: https://ghidra-sre.org/
   - Extract and run

2. **Install ghidra_nodejs plugin:**
   ```bash
   git clone https://github.com/P1sec/ghidra_nodejs
   # Copy the plugin to Ghidra's extensions directory
   cp -r ghidra_nodejs $GHIDRA_INSTALL_DIR/Ghidra/Extensions/
   ```

3. **Load the binary:**
   - Open Ghidra
   - Create new project
   - Import `chall.bin`
   - Analyze with Auto Analysis
   - The plugin should recognize V8 bytecode and decompile it

---

## Method 3: V8 Disassembler from Source

If you have V8 source or can build it:

```bash
# Get V8 source (this matches the NW.js version)
# For NW.js 0.99.0, find the corresponding V8 version

git clone https://chromium.googlesource.com/v8/v8.git
cd v8

# Build with disassembler enabled
tools/dev/gm.py x64.release

# Use d8 (V8 shell) with flags
./out/x64.release/d8 --print-bytecode your-script.js
```

However, this requires knowing the exact V8 version used by NW.js 0.99.0.

---

## Method 4: Hex Editor Analysis + Pattern Matching

```bash
# Look for V8 signature/magic bytes
xxd chall.bin | head -5

# The first bytes might indicate:
# - V8 version
# - Snapshot format
# - Compilation flags
```

Compare with known V8 snapshot formats to understand the structure.

---

## Method 5: Runtime Injection

Create a modified `chall.js` that intercepts the execution:

```javascript
// Save original evalNWBin
const originalEvalNWBin = nw.Window.get().evalNWBin;

// Override it
nw.Window.get().evalNWBin = function(a, b) {
    console.log("evalNWBin called with:", a, b);
    
    // Call original
    const result = originalEvalNWBin.call(this, a, b);
    
    // Now the code is loaded - inspect global scope
    console.log("Window object:", window);
    
    // Find all new functions
    for (let key in window) {
        if (typeof window[key] === 'function') {
            console.log("Function found:", key, window[key].toString());
        }
    }
    
    return result;
};

// Load normally
nw.Window.get().evalNWBin(null, 'chall.bin');
```

---

## Method 6: Memory Dump Analysis

Once the app is running:

1. **Get the process ID:**
   ```bash
   ps aux | grep nw
   ```

2. **Dump memory:**
   ```bash
   sudo gcore <PID>
   ```

3. **Search for JavaScript strings in the dump:**
   ```bash
   strings core.<PID> | grep -i "CJ{"
   strings core.<PID> | grep -i "function"
   strings core.<PID> | grep -i "sha\|hash"
   ```

---

## Recommended Approach (Step-by-Step)

### Quick Win Method:

1. **Start the app:**
   ```bash
   npm start
   ```

2. **Open DevTools (F12)**

3. **Go to Console tab and type:**
   ```javascript
   // Wait for the page to load, then:
   
   // Find the validation button
   var btn = document.getElementById('validateBtn');
   
   // Get its click handler
   console.log(btn.onclick);
   
   // Or get all event listeners
   getEventListeners(btn);
   ```

4. **Set a breakpoint:**
   - Go to Sources tab
   - Press `Ctrl+Shift+F` to search all files
   - Search for: `CORRECT FLAG` or `sha` or `hash`
   - This will show you the actual validation code!

5. **Alternative - Override the result:**
   ```javascript
   // In Console:
   var originalOnClick = document.getElementById('validateBtn').onclick;
   document.getElementById('validateBtn').onclick = function() {
       var input = document.getElementById('flagInput').value;
       console.log("Testing:", input);
       
       // Call original and log everything
       var result = originalOnClick.call(this);
       
       // Or just show success
       document.getElementById('result').textContent = 'CORRECT FLAG';
       document.getElementById('result').className = 'success';
   };
   ```

---

## Expected to Find

When you successfully decompile/inspect the code, you should find:

1. **The validation function** that:
   - Reads from `flagInput`
   - Performs some hash operation (SHA-256, SHA-512, or custom)
   - Compares against a hardcoded hash
   - Shows "CORRECT FLAG" or "INCORRECT FLAG"

2. **The actual flag** (possibly encoded or obfuscated)

3. **Alternative validation paths** or anti-debugging tricks

---

## Tools Summary

| Tool | Difficulty | Success Rate | Notes |
|------|-----------|--------------|-------|
| DevTools Dynamic Analysis | ★☆☆☆☆ | 95% | Best for beginners |
| Runtime Injection | ★★☆☆☆ | 90% | Good for understanding flow |
| View8 | ★★★☆☆ | 60% | May need format adjustments |
| Ghidra | ★★★★☆ | 70% | Powerful but complex |
| V8 Source Build | ★★★★★ | 80% | Most accurate but time-consuming |

**Recommendation:** Start with DevTools dynamic analysis!
