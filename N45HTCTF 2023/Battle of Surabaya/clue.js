function pwd_func() {
  var pwd = [
    "5NfBPeN",
    "854268mXCKSQ",
    "1GCfHrl",
    "8tPDcfl",
    "2331783UHWEEM",
    "3eiORmz",
    "24hYUCHs",
    "1884522pFNgpJ",
    "12402150OukXss",
    "222509JGAMTo",
    "4967644yKixeM",
    "2515474MDHUYo",
    "A really nice quote by Bung Tomo. But, somehow the server doesn't like quotes.",
  ]
  pwd_func = function () {
    return pwd
  }
  return pwd_func()
}
function get_pwd(_0x15daaa, _0x395bb0) {
  var pwd = pwd_func()
  get_pwd = function (idx, _0x59a24e) {
    idx = idx - 433
    var pwd_at_index = pwd[idx]
    return pwd_at_index
  }
  return get_pwd(_0x15daaa, _0x395bb0)
}
var _0x1a889d = get_pwd
;(function (_0x28aba8, _0x45c9bf) {
  var _0x1b6518 = _0x28aba8()
  while (true) {
    try {
      var _0x276c9d =
        (-parseInt(get_pwd(434)) / 0x1) * (-parseInt(get_pwd(443)) / 0x2) +
        (parseInt(get_pwd(437)) / 0x3) * (-parseInt(get_pwd(433)) / 0x4) +
        (parseInt(get_pwd(445)) / 0x5) * (-parseInt(get_pwd(439)) / 0x6) +
        (parseInt(get_pwd(441)) / 0x7) * (parseInt(get_pwd(435)) / 0x8) +
        parseInt(get_pwd(436)) / 0x9 +
        -parseInt(get_pwd(440)) / 0xa +
        (-parseInt(get_pwd(442)) / 0xb) * (-parseInt(get_pwd(438)) / 0xc)
      if (_0x276c9d === _0x45c9bf) {
        break
      } else {
        _0x1b6518.push(_0x1b6518.shift())
      }
    } catch (_0x275e32) {
      _0x1b6518.push(_0x1b6518.shift())
    }
  }
})(pwd_func, 0xa6fae)
// alert(
//   "A really nice quote by Bung Tomo. But, somehow the server doesn't like quotes."
// )
var _0x276c9d =
  (-parseInt(get_pwd(434)) / 0x1) * (-parseInt(get_pwd(443)) / 0x2) +
  (parseInt(get_pwd(437)) / 0x3) * (-parseInt(get_pwd(433)) / 0x4) +
  (parseInt(get_pwd(445)) / 0x5) * (-parseInt(get_pwd(439)) / 0x6) +
  (parseInt(get_pwd(441)) / 0x7) * (parseInt(get_pwd(435)) / 0x8) +
  parseInt(get_pwd(436)) / 0x9 +
  -parseInt(get_pwd(440)) / 0xa +
  (-parseInt(get_pwd(442)) / 0xb) * (-parseInt(get_pwd(438)) / 0xc)
console.log(_0x276c9d)
console.log(pwd_func())
