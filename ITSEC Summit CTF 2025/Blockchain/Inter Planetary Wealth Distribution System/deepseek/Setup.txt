// SPDX-License-Identifier: INJU
pragma solidity ^0.8.28;

import "./IPWD.sol";
import "./IPWDAdministrator.sol";
import "./Validator.sol";
import "./ValidatorInterface.sol";

contract Setup{

    Validator public validator;
    ValidatorInterface public vi;
    IPWD public ipwd;
    IPWDAdministrator public ipwdAdmin;
    address public player;

    constructor(bytes32[] memory _referalCode) payable {
        vi = new ValidatorInterface();
        validator = vi.validator();
        ipwd = new IPWD(false);
        ipwdAdmin = new IPWDAdministrator{value: 2000 ether}(_referalCode, address(ipwd), address(vi));

        ipwd.setAdministrator(address(ipwdAdmin));
    }

    function setPlayer() external{
        require(!ipwd.isSmartContract(msg.sender), "EOA Only");
        player = msg.sender;
    }

    function isSolved() public view returns(bool){
        return (
            address(ipwdAdmin).balance == 0 &&
            address(player).balance >= 2001 ether &&
            ipwd.allowAllContracts() == false &&
            ipwd.balanceOf(address(ipwdAdmin)) >= 2000 ether
        );  
    }
}