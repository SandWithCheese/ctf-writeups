enc = []
holder1 = []
holder2 = []

// charCodeAt == ord
fl4g.split("").map((x, y) => {
  !y
    ? (holder1[y] = x.charCodeAt(0) + 1)
    : (holder1[y] = (x.charCodeAt(0) + holder1[y - 1]) % ((2 ** 9) << 16))
})

holder1.map((e, i) => {
  !i
    ? (holder2[i] = holder1[i])
    : (holder2[i] = (e + holder1[i - 1]) % ((2 ** 9) << 8))
})

enc = holder1.concat(holder2)
enc.map((e, i) => {
  enc[i] = String.fromCharCode(e)
})
enc = enc.join("")
