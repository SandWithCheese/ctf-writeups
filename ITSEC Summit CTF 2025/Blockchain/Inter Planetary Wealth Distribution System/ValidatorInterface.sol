// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.28;

import "./Validator.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ValidatorInterface is Ownable{
    Validator public validator;

    bool public claimToken = false;

    mapping(address => bool) public validated;
    mapping(address => bool) public isIPWDAllow;
    mapping(address => uint256) public validatedCount;

    constructor() Ownable(msg.sender){
        validator = new Validator();
    }

    function claimValidatorToken() public {
        require(!claimToken, "Claimed");
        claimToken = true;
        validator.transfer(msg.sender, 1);
    }

    function giveValidation(address _toValidate) external {
        require(_toValidate != msg.sender, "VALIDATOR: Cannot self-validate");
        require(validator.balanceOf(msg.sender) == 1, "VALIDATOR: Require a Token to Vote!");
        require(!validated[msg.sender], "VALIDATOR: already submit for Validation!");
        validated[msg.sender] = true;
        if (_toValidate == address(0)){
            validatedCount[msg.sender] = 0;
        }else{
            validatedCount[_toValidate]+= 1;
        }
    }

    function clearOfValidation() external {
        require(_getValidationCount(msg.sender) >= 10, "VALIDATOR: Required Point of at least 10");
        isIPWDAllow[msg.sender] = true;
    }

    function isAllowToRegisterAtIPWD(address _addr) public view returns(bool){
        return _isAllowToRegisterAtIPWD(_addr);
    }

    function getValidationCount(address _addr) external view returns(uint256){
        return _getValidationCount(_addr);
    }

    function _isAllowToRegisterAtIPWD(address _addr) internal view returns(bool){
        return isIPWDAllow[_addr];
    }

    function _getValidationCount(address _addr) internal view returns(uint256){
        return validatedCount[_addr];
    }

}