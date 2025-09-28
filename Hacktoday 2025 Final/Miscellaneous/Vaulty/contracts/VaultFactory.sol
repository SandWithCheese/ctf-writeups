// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Vault.sol";
import "./Token.sol";
import "./lib/ERC20.sol";

contract VaultFactory {

    address immutable public CHALLENGE;

	Vault[] public allVaults;

    constructor(address _challenge) {
        CHALLENGE = _challenge;
    }


    function deploy(uint[][] memory params) public {
        
        for (uint256 i = 0; i < params.length; i++) {
            for(uint256 j = 0; j < params[i].length; j++) {
                require(params[i][j] > 0, "parameter must greater than 0");
            }
            Token asset = new Token(CHALLENGE);
            Vault vault = new Vault(ERC20(asset), params[i]);

            allVaults.push(vault);
        }
	}

	function numVaults() external view returns (uint256) {
		return allVaults.length;
	}

	function vaultAt(uint256 index) external view returns (Vault) {
		return allVaults[index];
	}
}


