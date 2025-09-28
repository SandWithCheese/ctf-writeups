// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./VaultFactory.sol";
import "./Vault.sol";

import "./Token.sol";


contract Setup {

    VaultFactory public vaultFactory;

    constructor() payable {
        vaultFactory = new VaultFactory(address(this));
    }

    function isSolved() public returns(bool) {

        Vault vault = Vault(vaultFactory.vaultAt(0));
        if(address(vault) == address(0)) return false;

        // helper function to simulate the challenge token minting
        Token(address(vault.asset())).mintToChallenge();

        vault.asset().approve(address(vault), type(uint256).max);
        vault.deposit(800 ether, address(this));

        if(vault.balanceOf(address(this)) == 0) return true;

        return false;
    }
}