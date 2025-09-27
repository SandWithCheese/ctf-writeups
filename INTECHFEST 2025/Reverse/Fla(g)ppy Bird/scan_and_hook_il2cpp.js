"use strict"

// Minimal helper to read C strings/UTF8
function readCString(ptr) {
  if (ptr.isNull()) return ""
  return ptr.readUtf8String()
}

const KWS = [
  "Score",
  "score",
  "Points",
  "points",
  "Flag",
  "flag",
  "Win",
  "win",
  "TMP_Text",
  "Text",
]

function containsKW(s) {
  return KWS.some((k) => s.indexOf(k) !== -1)
}

function addr(name) {
  const m = Module.findExportByName("libil2cpp.so", name)
  if (!m) {
    throw new Error("Missing export: " + name)
  }
  return m
}

// Resolve IL2CPP exports (we saw many of these strings in libil2cpp.so)
const il2cpp_domain_get = new NativeFunction(
  addr("il2cpp_domain_get"),
  "pointer",
  []
)
const il2cpp_domain_get_assemblies = new NativeFunction(
  addr("il2cpp_domain_get_assemblies"),
  "void",
  ["pointer", "pointer", "pointer"]
)
const il2cpp_assembly_get_image = new NativeFunction(
  addr("il2cpp_assembly_get_image"),
  "pointer",
  ["pointer"]
)
const il2cpp_image_get_name = new NativeFunction(
  addr("il2cpp_image_get_name"),
  "pointer",
  ["pointer"]
)
const il2cpp_image_get_class_count = new NativeFunction(
  addr("il2cpp_image_get_class_count"),
  "uint64",
  ["pointer"]
)
const il2cpp_image_get_class = new NativeFunction(
  addr("il2cpp_image_get_class"),
  "pointer",
  ["pointer", "uint64"]
)
const il2cpp_class_get_name = new NativeFunction(
  addr("il2cpp_class_get_name"),
  "pointer",
  ["pointer"]
)
const il2cpp_class_get_namespace = new NativeFunction(
  addr("il2cpp_class_get_namespace"),
  "pointer",
  ["pointer"]
)
const il2cpp_class_get_methods = new NativeFunction(
  addr("il2cpp_class_get_methods"),
  "pointer",
  ["pointer", "pointer"]
)
const il2cpp_method_get_name = new NativeFunction(
  addr("il2cpp_method_get_name"),
  "pointer",
  ["pointer"]
)
const il2cpp_method_get_from_reflection = Module.findExportByName(
  "libil2cpp.so",
  "il2cpp_method_get_from_reflection"
)
  ? new NativeFunction(addr("il2cpp_method_get_from_reflection"), "pointer", [
      "pointer",
    ])
  : null
const il2cpp_method_get_pointer = new NativeFunction(
  addr("il2cpp_method_get_pointer"),
  "pointer",
  ["pointer"]
)
const il2cpp_string_chars = new NativeFunction(
  addr("il2cpp_string_chars"),
  "pointer",
  ["pointer"]
)
const il2cpp_string_length = new NativeFunction(
  addr("il2cpp_string_length"),
  "int",
  ["pointer"]
)

// Helper to convert Il2CppString* to JS string (UTF-16)
function il2cppStringToJs(strPtr) {
  if (strPtr.isNull()) return "(null)"
  const len = il2cpp_string_length(strPtr)
  const charsPtr = il2cpp_string_chars(strPtr)
  return charsPtr.readUtf16String(len)
}

// Wait for libil2cpp and then run
Module.ensureInitialized("libil2cpp.so")

function enumerateAll() {
  const domain = il2cpp_domain_get()
  // Get assemblies array
  const sizePtr = Memory.alloc(8)
  sizePtr.writeU64(0)
  const outPtrPtr = Memory.alloc(Process.pointerSize)
  il2cpp_domain_get_assemblies(domain, outPtrPtr, sizePtr)
  const count = sizePtr.readU64().toNumber()
  const arr = outPtrPtr.readPointer()

  console.log("[*] Assemblies:", count)
  const interesting = []

  for (let i = 0; i < count; i++) {
    const asm = arr.add(i * Process.pointerSize).readPointer()
    const img = il2cpp_assembly_get_image(asm)
    const imgName = readCString(il2cpp_image_get_name(img))
    const classCount = il2cpp_image_get_class_count(img)

    for (let ci = 0; ci < classCount.toNumber(); ci++) {
      const klass = il2cpp_image_get_class(img, ptr(ci))
      if (klass.isNull()) continue
      const ns = readCString(il2cpp_class_get_namespace(klass)) || ""
      const cn = readCString(il2cpp_class_get_name(klass)) || ""
      const fq = (ns.length ? ns + "." : "") + cn

      // enumerate methods
      const iterPtr = Memory.alloc(Process.pointerSize)
      iterPtr.writePointer(ptr(0))
      while (true) {
        const method = il2cpp_class_get_methods(klass, iterPtr)
        if (method.isNull()) break
        const mn = readCString(il2cpp_method_get_name(method)) || ""
        const sig = fq + "::" + mn

        if (containsKW(fq) || containsKW(mn)) {
          interesting.push(sig)
        }
      }
    }
  }

  console.log("[*] --- Interesting methods/classes ---")
  interesting.slice(0, 4000).forEach((s) => console.log(s))
  console.log("[*] -----------------------------------")
  return interesting
}

// Find a method pointer by exact class & method name match
function findMethodPointer(targets) {
  const domain = il2cpp_domain_get()
  const sizePtr = Memory.alloc(8)
  const outPtrPtr = Memory.alloc(Process.pointerSize)
  il2cpp_domain_get_assemblies(domain, outPtrPtr, sizePtr)
  const count = sizePtr.readU64().toNumber()
  const arr = outPtrPtr.readPointer()

  function match(name, arr) {
    return arr.some((t) => name.indexOf(t) >= 0)
  }

  for (let i = 0; i < count; i++) {
    const asm = arr.add(i * Process.pointerSize).readPointer()
    const img = il2cpp_assembly_get_image(asm)
    const classCount = il2cpp_image_get_class_count(img)

    for (let ci = 0; ci < classCount.toNumber(); ci++) {
      const klass = il2cpp_image_get_class(img, ptr(ci))
      if (klass.isNull()) continue
      const ns = readCString(il2cpp_class_get_namespace(klass)) || ""
      const cn = readCString(il2cpp_class_get_name(klass)) || ""
      const fq = (ns.length ? ns + "." : "") + cn

      const iterPtr = Memory.alloc(Process.pointerSize)
      iterPtr.writePointer(ptr(0))
      while (true) {
        const method = il2cpp_class_get_methods(klass, iterPtr)
        if (method.isNull()) break
        const mn = readCString(il2cpp_method_get_name(method)) || ""
        const sig = fq + "::" + mn

        if (targets.some((t) => sig.indexOf(t) >= 0)) {
          const fn = il2cpp_method_get_pointer(method)
          if (!fn.isNull()) {
            return { sig, fn }
          }
        }
      }
    }
  }
  return null
}

function hookSetText() {
  const candidates = [
    "UnityEngine.UI.Text::set_text",
    "TMPro.TMP_Text::set_text",
  ]
  const found = findMethodPointer(candidates)
  if (!found) {
    console.log("[-] Could not locate Text.set_text / TMP_Text.set_text")
    return
  }
  console.log("[+] Hooking", found.sig, "at", found.fn)

  Interceptor.attach(found.fn, {
    onEnter(args) {
      // thiscall: arg0 = this, arg1 = Il2CppString*
      try {
        const str = il2cppStringToJs(args[1])
        if (str && str.length) {
          // Only log if looks like score-ish or contains "flag"
          if (/^\d+$/.test(str) || /flag/i.test(str) || /score/i.test(str)) {
            console.log(`[UI TEXT] ${found.sig} -> "${str}"`)
            console.log(
              Thread.backtrace(this.context, Backtracer.ACCURATE)
                .map(DebugSymbol.fromAddress)
                .join("\n")
            )
            console.log("----")
          }
        }
      } catch (e) {}
    },
  })
}

function main() {
  console.log("[*] Starting IL2CPP scan...")
  const list = enumerateAll()
  // Print top ~100 relevant items now (already printed)
  hookSetText()
}

main()
