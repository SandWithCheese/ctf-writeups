// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./lib/ERC20.sol";

contract Token is ERC20 {

    address immutable public CHALLENGE;

    bool public mintedToPlayer = false;
    bool public mintedToChallenge = false;
    constructor(address _challenge) ERC20("Token", "TKN") {
        CHALLENGE = _challenge;
    }

    function mintToPlayer() public {
        require(!mintedToPlayer, "Player already minted");
        _mint(msg.sender, 1_000 ether);
        mintedToPlayer = true;
    }

    function mintToChallenge() public {
        require(!mintedToChallenge, "Challenge already minted");
        _mint(CHALLENGE, 1_000 ether);
        mintedToChallenge = true;
    }
}


