// Decode the first obfuscated string (URL)
const _0x1b8a4e = [
  104, 116, 116, 112, 115, 58, 47, 47, 103, 105, 116, 104, 117, 98, 46, 99, 111,
  109, 47, 107, 101, 110, 115, 104, 105, 57, 57, 121, 47, 105, 109, 97, 103,
  101, 45, 100, 111, 119, 110, 108, 111, 97, 100, 101, 114, 47, 114, 97, 119,
  47, 114, 101, 102, 115, 47, 104, 101, 97, 100, 115, 47, 109, 97, 105, 110, 47,
  82, 117, 110, 77, 101, 46, 101, 120, 101,
]
console.log("URL:", String.fromCharCode(..._0x1b8a4e))

// Decode the second obfuscated string (filename)
const _0x3e8f7c = [82, 117, 110, 77, 101]
console.log("Filename:", String.fromCharCode(..._0x3e8f7c))

// Decode the third obfuscated string (flag)
const _0x1f9a8c = [
  101, 101, 102, 117, 102, 115, 115, 120, 101, 101, 95, 95, 97, 111, 48, 110,
  51, 95, 51, 110, 115, 98, 108, 97, 111, 102, 98, 49, 114, 50, 125, 48, 51,
  100, 99, 116, 95, 115, 117, 48, 56, 110,
]
const _0x4b7d2e = [
  1, 39, 31, 7, 11, 26, 15, 18, 5, 30, 9, 27, 35, 10, 28, 21, 36, 16, 17, 25,
  14, 0, 8, 3, 24, 6, 34, 23, 4, 37, 41, 38, 20, 32, 2, 19, 12, 13, 33, 29, 40,
  22,
]
const _0x3c6a5d = new Array(_0x1f9a8c.length)
for (let i = 0; i < _0x1f9a8c.length; i++) {
  _0x3c6a5d[_0x4b7d2e[i]] = _0x1f9a8c[i]
}
console.log("Flag:", String.fromCharCode(..._0x3c6a5d))
