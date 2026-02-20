// Instrumented version of chall.js for reverse engineering
// This intercepts and logs everything the binary does

console.log("[*] Starting instrumented chall.js")

// Save original evalNWBin
const originalEvalNWBin = nw.Window.get().evalNWBin

// Track what gets added to window
const beforeKeys = new Set(Object.keys(window))

// Override evalNWBin to intercept
nw.Window.get().evalNWBin = function (a, b) {
  console.log("[*] evalNWBin called with args:", a, b)
  console.log("[*] Loading binary:", b)

  // Call original
  const result = originalEvalNWBin.call(this, a, b)

  console.log("[*] Binary loaded successfully")

  // Find what was added to window
  const afterKeys = Object.keys(window)
  const newKeys = afterKeys.filter((k) => !beforeKeys.has(k))

  console.log("[*] New global variables/functions:", newKeys)

  // Log all new functions
  newKeys.forEach((key) => {
    if (typeof window[key] === "function") {
      console.log(`[FUNCTION] ${key}:`, window[key].toString())
    } else {
      console.log(`[VARIABLE] ${key}:`, window[key])
    }
  })

  // Wait for DOM to be ready, then intercept the button
  window.addEventListener("DOMContentLoaded", function () {
    console.log("[*] DOM loaded, setting up button interception")

    const btn = document.getElementById("validateBtn")
    if (btn) {
      // Store original handler
      const originalHandler = btn.onclick

      // Replace with instrumented version
      btn.onclick = function (e) {
        const input = document.getElementById("flagInput").value
        console.log("[*] Validate button clicked!")
        console.log("[*] Input flag:", input)

        // You can modify the flag here for testing
        // document.getElementById('flagInput').value = "CJ{test}";

        // Call original handler
        if (originalHandler) {
          console.log("[*] Calling original handler...")
          try {
            const result = originalHandler.call(this, e)
            console.log("[*] Handler result:", result)
          } catch (err) {
            console.error("[!] Error in handler:", err)
          }
        } else {
          console.warn("[!] No original handler found")
        }

        // Log the result
        setTimeout(() => {
          const resultEl = document.getElementById("result")
          console.log("[*] Validation result:", resultEl.textContent)
          console.log("[*] Result class:", resultEl.className)
        }, 100)
      }

      console.log("[*] Button interception ready")

      // If there's a click event listener instead of onclick
      const listeners = getEventListeners ? getEventListeners(btn) : null
      if (listeners) {
        console.log("[*] Event listeners on button:", listeners)
      }
    } else {
      console.warn("[!] Validate button not found")
    }
  })

  return result
}

// Now load the binary
nw.Window.get().evalNWBin(null, "chall.bin")

console.log("[*] Instrumentation complete")

// Helper function to dump all variables
window.dumpAll = function () {
  console.log("=== GLOBAL SCOPE DUMP ===")
  for (let key in window) {
    if (window.hasOwnProperty(key)) {
      const value = window[key]
      const type = typeof value

      if (type === "function") {
        console.log(
          `${key} [function]:`,
          value.toString().substring(0, 100) + "..."
        )
      } else {
        console.log(`${key} [${type}]:`, value)
      }
    }
  }
}

// Helper to test flags
window.testFlag = function (flag) {
  document.getElementById("flagInput").value = flag
  document.getElementById("validateBtn").click()
}

console.log("[*] Helper functions available: dumpAll(), testFlag(flag)")
