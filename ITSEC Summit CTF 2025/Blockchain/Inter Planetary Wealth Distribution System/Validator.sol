// SPDX-License-Identifier: INJU
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Validator is ERC20, Ownable{

    constructor() ERC20("Validator", "VLDTR") Ownable(msg.sender){
        _mint(address(owner()), 100);
    }

    function mint(address _to, uint256 amount) external onlyOwner{
        _mint(_to, amount);
    }

}