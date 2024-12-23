/*
This file is part of web3.js.

web3.js is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

web3.js is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with web3.js.  If not, see <http://www.gnu.org/licenses/>.
*/
export var Transport;
(function (Transport) {
    Transport["HTTPS"] = "https";
    Transport["WebSocket"] = "wss";
})(Transport || (Transport = {}));
;
export var Network;
(function (Network) {
    Network["ETH_MAINNET"] = "eth_mainnet";
    Network["ETH_GOERLI"] = "eth_goerli";
    Network["ETH_SEPOLIA"] = "eth_sepolia";
    Network["ETH_HOLESKY"] = "eth_holesky";
    Network["POLYGON_MAINNET"] = "polygon_mainnet";
    Network["POLYGON_MUMBAI"] = "polygon_mumbai";
    Network["POLYGON_AMONY"] = "polygon_amony";
    Network["ARBITRUM_MAINNET"] = "arbitrum_mainnet";
    Network["ARBITRUM_SEPOLIA"] = "arbitrum_sepolia";
    Network["BASE_MAINNET"] = "base_mainnet";
    Network["BASE_SEPOLIA"] = "base_sepolia";
    Network["OPTIMISM_MAINNET"] = "optimism_mainnet";
    Network["OPTIMISM_SEPOLIA"] = "optimism_sepolia";
    Network["BNB_MAINNET"] = "bnb_mainnet";
    Network["BNB_TESTNET"] = "bnb_testnet";
})(Network || (Network = {}));
;
//# sourceMappingURL=types.js.map