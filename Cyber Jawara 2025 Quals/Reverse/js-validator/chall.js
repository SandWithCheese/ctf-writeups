// Auto-dumping instrumented version - logs to console and file
console.log("[*] Auto-dump instrumented chall.js starting...")

// Save original evalNWBin
const originalEvalNWBin = nw.Window.get().evalNWBin

// Track what's in window before
const beforeKeys = new Set(Object.keys(window))

// Storage for captured data
window._dumpData = {
  functions: {},
  variables: {},
  validationCode: null,
}

// Override evalNWBin
nw.Window.get().evalNWBin = function (a, b) {
  console.log("[*] Loading binary:", b)

  // Call original
  const result = originalEvalNWBin.call(this, a, b)

  console.log("[*] Binary loaded, capturing data...")

  // Find what was added
  const afterKeys = Object.keys(window)
  const newKeys = afterKeys.filter((k) => !beforeKeys.has(k))

  console.log("[*] New items found:", newKeys.length)

  // Capture everything
  newKeys.forEach((key) => {
    try {
      const value = window[key]
      if (typeof value === "function") {
        const code = value.toString()
        window._dumpData.functions[key] = code
        console.log(`[FUNCTION] ${key}`)
        console.log(code)
        console.log("---")
      } else {
        window._dumpData.variables[key] = String(value)
        console.log(`[VARIABLE] ${key} = ${value}`)
      }
    } catch (e) {
      console.log(`[ERROR] Could not capture ${key}:`, e.message)
    }
  })

  // Wait for DOM, then capture button handler
  setTimeout(() => {
    console.log("[*] Attempting to capture button handler...")

    const btn = document.getElementById("validateBtn")
    if (btn && btn.onclick) {
      const validationCode = btn.onclick.toString()
      window._dumpData.validationCode = validationCode

      console.log("[*] ===== VALIDATION FUNCTION FOUND =====")
      console.log(validationCode)
      console.log("[*] ========================================")

      // Try to write to file via Node.js
      try {
        const fs = require("fs")
        const output = {
          timestamp: new Date().toISOString(),
          functions: window._dumpData.functions,
          variables: window._dumpData.variables,
          validationCode: window._dumpData.validationCode,
        }

        fs.writeFileSync("reverse_dump.json", JSON.stringify(output, null, 2))
        console.log("[*] Data saved to: reverse_dump.json")
      } catch (e) {
        console.log("[!] Could not write to file:", e.message)
        console.log("[*] But all data is in window._dumpData")
      }
    } else {
      console.log("[!] Button or onclick not found")

      // Try to get event listeners
      setTimeout(() => {
        try {
          // Look for validation-related functions in global scope
          for (let key in window) {
            if (typeof window[key] === "function") {
              const fname = key.toLowerCase()
              if (
                fname.includes("valid") ||
                fname.includes("check") ||
                fname.includes("hash") ||
                fname.includes("sha")
              ) {
                console.log(`[*] Found potential validation function: ${key}`)
                console.log(window[key].toString())
              }
            }
          }
        } catch (e) {
          console.log("[!] Error searching for functions:", e)
        }
      }, 100)
    }
  }, 500)

  return result
}

// Load the binary
nw.Window.get().evalNWBin(null, "chall.bin")

console.log("[*] Instrumentation complete!")
console.log("[*] Check window._dumpData for captured information")
console.log("[*] Check reverse_dump.json for saved output")
