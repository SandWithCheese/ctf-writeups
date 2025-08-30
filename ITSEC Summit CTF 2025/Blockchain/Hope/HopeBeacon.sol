// SPDX-License-Identifier: Kiinzu
pragma solidity 0.8.28;

import { ERC1967Proxy } from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract HopeBeacon is ERC1967Proxy{
    constructor(address _implementation, bytes memory _data) ERC1967Proxy(_implementation, _data){}
}