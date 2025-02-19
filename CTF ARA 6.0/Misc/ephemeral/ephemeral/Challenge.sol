pragma solidity ^0.8.0;

contract Challenge {
	address public owner;

	constructor() {
		owner = msg.sender;
	}

	function getOwnership(address account) external {
		assembly {
			let size := extcodesize(caller())
			if iszero(eq(size, 0)) {
				revert(0, 0)
			}
			let why := staticcall(gas(), account, 0, 0, 0, 0x20)
			
			if iszero(eq(returndatasize(), 0x20)) {
				revert(0, 0)
			}
			returndatacopy(0, 0, 0x20)
			sstore(0, mload(0))
		}
	}

	function transferOwnership(address newOwner) external {
		require(msg.sender == owner, "Not owner");
		owner = newOwner;
	}
}