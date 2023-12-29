function generate() {
  const _0x4eebc6 = (function () {
    let _0x30f6f4 = true
    return function (_0x42d033, _0x11727c) {
      const _0x1da2d6 = _0x30f6f4
        ? function () {
            if (_0x11727c) {
              const _0x51f94a = _0x11727c.apply(_0x42d033, arguments)
              _0x11727c = null
              return _0x51f94a
            }
          }
        : function () {}
      _0x30f6f4 = false
      return _0x1da2d6
    }
  })()
  const _0x424949 = _0x4eebc6(this, function () {
    return _0x424949
      .toString()
      .search("(((.+)+)+)+$")
      .toString()
      .constructor(_0x424949)
      .search("(((.+)+)+)+$")
  })
  _0x424949()
  const _0x904378 = (function () {
    let _0x225c57 = true
    return function (_0x1cc4a2, _0x245a05) {
      const _0x10ddc1 = _0x225c57
        ? function () {
            if (_0x245a05) {
              const _0x153ece = _0x245a05.apply(_0x1cc4a2, arguments)
              _0x245a05 = null
              return _0x153ece
            }
          }
        : function () {}
      _0x225c57 = false
      return _0x10ddc1
    }
  })()
  const _0x396cdd = _0x904378(this, function () {
    const _0xa4efec = function () {
      let _0x45fce4
      try {
        _0x45fce4 = Function(
          'return (function() {}.constructor("return this")( ));'
        )()
      } catch (_0x1ea28b) {
        _0x45fce4 = window
      }
      return _0x45fce4
    }
    const _0xe0798 = _0xa4efec()
    const _0x709357 = (_0xe0798.console = _0xe0798.console || {})
    const _0x5b8732 = [
      "log",
      "warn",
      "info",
      "error",
      "exception",
      "table",
      "trace",
    ]
    for (let _0x3e68d3 = 0x0; _0x3e68d3 < _0x5b8732.length; _0x3e68d3++) {
      const _0x31145c = _0x904378.constructor.prototype.bind(_0x904378)
      const _0x33bb1a = _0x5b8732[_0x3e68d3]
      const _0x5a5d54 = _0x709357[_0x33bb1a] || _0x31145c
      _0x31145c.__proto__ = _0x904378.bind(_0x904378)
      _0x31145c.toString = _0x5a5d54.toString.bind(_0x5a5d54)
      _0x709357[_0x33bb1a] = _0x31145c
    }
  })
  _0x396cdd()
  return Math.floor(Math.random() * 256 + 0x0)
}
let randoms = []
for (let i = 0x0; i < 0x8; i++) {
  randoms.push(generate())
}
for (
  let i = 0x0;
  i < "CTFITB{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}".length;
  i++
) {
  console.log(
    "CTFITB{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}"[i] ^ randoms[i % 0x8]
  )
}
