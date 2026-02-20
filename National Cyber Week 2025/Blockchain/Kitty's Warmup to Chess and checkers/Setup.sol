// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./KittyWarmup.sol";
import "./Token.sol";

contract Setup {
    KittyWarmup public immutable kitty;
    Token public immutable token;

    address public player;
    uint256 public immutable initialRewardBalance;

    constructor() {
        token = new Token(1e30);
        kitty = new KittyWarmup(IERC20(address(token)));

        uint256 amount = 1e27;
        token.transfer(address(kitty), amount);
        initialRewardBalance = amount;
    }

    function setPlayer(address _player) external {
        require(player == address(0), "player already set");
        require(_player != address(0), "invalid player");

        player = _player;

        kitty.seedAllocation(player, 100);
    }

    function isSolved() external view returns (bool) {
        if (player == address(0)) {
            return false;
        }

        uint256 targetAmount = uint256(kitty.TARGET_POINTS()) *
            kitty.POINT_TO_TOKEN();

        return token.balanceOf(player) >= targetAmount * 2;
    }
}
