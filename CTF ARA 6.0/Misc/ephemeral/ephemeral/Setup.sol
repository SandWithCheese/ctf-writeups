// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import {Challenge} from "./Challenge.sol";

interface IChallenge {
	function owner() external view returns (address);
}

contract Setup {
	address public player;
	address public challenge;

	constructor(address _player) payable {
		player = _player;
		
		payable(player).transfer(msg.value);
		
		// Challenge deployment
		challenge = address(new Challenge());
	}

	function isSolved() external view returns (bool) {
		return IChallenge(challenge).owner() == player;
	}
}