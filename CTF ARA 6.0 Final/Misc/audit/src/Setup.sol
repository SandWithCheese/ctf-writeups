// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import {Carbon} from "./Carbon.sol";

interface IChallenge {
	function owner() external view returns (address);
}

contract Setup {
	address public player;
	address public challenge;
	bool public destroyed;

	constructor(address _player) payable {
		player = _player;
		
		payable(player).transfer(msg.value);
		
		// Challenge deployment
		challenge = address(new Carbon());
	}

	function destroy() external {
		require(msg.sender == player && tx.origin == player, "Player-only function");
		destroyed = true;
	}

	function isSolved() external view returns (bool) {
		return IChallenge(challenge).owner() == player;
	}
}
