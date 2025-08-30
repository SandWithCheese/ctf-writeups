// SPDX-License-Identifier: INJU
pragma solidity ^0.8.28;

contract Multicall {
    
    function multicall(bytes[] calldata data) external payable returns (bytes[] memory results) {
        results = new bytes[](data.length);
        for (uint256 i = 0; i < data.length; i++) {
            results[i] = doDelegateCall(data[i]);
        }
        return results;
    }

    function doDelegateCall(bytes memory data) private returns (bytes memory) {
        (bool success, bytes memory res) = address(this).delegatecall(data);

        if (!success) {
            revert(string(res));
        }

        return res;
    }
    
}