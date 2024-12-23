// SPDX-License-Identifier: MTI
pragma solidity ^0.8.0;

import "Locket.sol";

contract Setup {
    Locket public locket;
    constructor() payable {
        locket = new Locket{value: 30 ether}();
    }

    function isSolved() external view returns (bool) {
        return locket.isSolved();
    }
}
