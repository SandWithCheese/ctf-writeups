const { ethers } = require("ethers")
;(async () => {
  const RPC =
    "http://103.226.138.119:24379/d396cc43-4679-4af2-9725-44e25dfd0a6f"
  const provider = new ethers.providers.JsonRpcProvider(RPC)
  const txHash =
    "0xcbededac7468f5a2318c546fbf17f01d9a3980bae0a4bf24213a8a121c549e31" // replace with your isSolved() tx hash
  const r = await provider.getTransactionReceipt(txHash)
  console.log(r)
})()
