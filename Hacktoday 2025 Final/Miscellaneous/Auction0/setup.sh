export RPC_URL="http://103.226.138.119:1169/2fff5963-9c1d-4b48-a304-10f02db97c3c"
export PRIVKEY="52c2884b1d1271380bdfb875721886943893392f7dd88b7275dbafc20a4abb59"
export SETUP_ADDR="0x9174265927fc4675AE397dcf879E1E0722Bc4Ecf"
export WALLET_ADDR="0x2F991C204eceeC639Cc14b01F37Cfb43143cD922"

cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "auction()"
cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "nft()"
cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "tokenId()"

export AUCTION_ADDR=$(cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "auction()" | tr -d '\r')
export NFT_ADDR=$(cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "nft()" | tr -d '\r')
export TOKEN_ID=$(cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "tokenId()" | tr -d '\r')
echo $AUCTION_ADDR
echo $NFT_ADDR
echo $TOKEN_ID

# endTime, lastBidder, uniqueBidders, current balance (via Balance())
cast call --rpc-url $RPC_URL --to $AUCTION_ADDR --function "endTime()"
cast call --rpc-url $RPC_URL --to $AUCTION_ADDR --function "lastBidder()"
cast call --rpc-url $RPC_URL --to $AUCTION_ADDR --function "uniqueBidders()"
cast call --rpc-url $RPC_URL --to $AUCTION_ADDR --function "Balance()"

cast call --rpc-url $RPC_URL --to $SETUP_ADDR --function "isSolved()" || true

