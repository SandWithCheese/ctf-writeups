// SPDX-License-Identifier: INJU
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/access/Ownable.sol";
import {ValidatorInterface} from "./ValidatorInterface.sol";
import {Multicall} from "./Multicall.sol";
import {IPWD} from "./IPWD.sol";

contract IPWDAdministrator is Multicall, Ownable{

    IPWD public ipwd;
    ValidatorInterface public vi;

    bytes32[] private referralCode;

    uint256 public referralCounts;
    uint256 public FEE_TO_REGISTER;

    mapping(address => bool) public referralRedeemer;
    mapping(address => uint) public referralCounter;
    mapping(bytes32 => address) public referralOwner;
    mapping(address => uint256) public lockPeriod;
    mapping(address => bool) public onLockPeriod;
    mapping(address => bool) public member;

    error notListed(address toCheck);
    error notReferralOwner(address toCheck);
    error notMemberPurchaseAttempt(address toCheck);
    error allAssetisLocked(address toCheck);

    constructor(
        bytes32[] memory _referral,
        address _ipwdAddress,
        address _validatorInterface
    ) Ownable(msg.sender) payable {
        vi = ValidatorInterface(_validatorInterface);
        ipwd = IPWD(_ipwdAddress);
        referralCode = _referral;
        referralCounts = 0;
        FEE_TO_REGISTER = 2 ether;
    }

    function claimReferral() external returns(bytes32) {
        require(vi.isAllowToRegisterAtIPWD(msg.sender) == true, "IPWD: Clearance is not premitted");
        require(!referralRedeemer[msg.sender], "IPWD: Already claimed referral code");
        require(tx.origin == msg.sender, "IPWD: Member of Bank is restricted to EOA");
        uint256 referralToReturn = referralCounts;
        referralRedeemer[msg.sender] = true;
        referralCounter[msg.sender] = referralToReturn;
        referralOwner[referralCode[referralToReturn]] = msg.sender;
        referralCounts += 1;
        return referralCode[referralToReturn];
    }

    function register(bytes32 _referral) external payable{
        require(vi.isAllowToRegisterAtIPWD(msg.sender) == true, "IPWD: Clearance is not premitted");
        require(referralValidator(_referral));
        require(msg.value == FEE_TO_REGISTER, "IPWD: Please pay the Administration Fee.");
        member[msg.sender] = true;
    }

    function referAFriend(bytes32 _referral, address _recipient) external payable onlyMember{
        require(msg.value == FEE_TO_REGISTER, "IPWD: Please pay the Administration Fee.");
        require(referralOwner[_referral] == address(0x0), "IPWD: Referral is used.");
        member[_recipient] = true;
    }

    function mintToken(address _to) external payable onlyMember{
        if(!isMember(_to)){
            revert notMemberPurchaseAttempt(_to);
        }
        ipwd.mint(_to, msg.value);
    }

    function sellToken(uint256 _amount) external onlyMember{
        require(ipwd.getBalance(msg.sender) >= _amount, "IPWD: Not enough tokens");
        require(_amount <= 505 ether, "IPWD: Limit per sell attempt is 500 Ether");
        if(isLocked(msg.sender)){
            revert allAssetisLocked(msg.sender);
        }
        lockPeriod[msg.sender] += 365 days;
                
        bool success = ipwd.transferFrom(msg.sender, address(this), _amount);
        require(success, "IPWD: Transfer failed");        
    
        (bool sent, ) = msg.sender.call{value: _amount}("");
        require(sent);
    }

    // internal functions
    function referralValidator(bytes32 _referral) internal view returns(bool){
        if(!referralRedeemer[msg.sender]){
            revert notListed(msg.sender);
        }
        if(msg.sender != referralOwner[_referral]){
            revert notReferralOwner(msg.sender);
        }
        bytes32 senderReferral = referralCode[referralCounter[msg.sender]];
        return _referral == senderReferral ? true : false;
    }

    function currentHoldings() internal view returns(bool){
        uint256 currentBalance = ipwd.getBalance(msg.sender);
        return currentBalance <= 500 ether;
    }

    function isLocked(address _addr) internal returns(bool){
        if(lockPeriod[_addr] == 0){
            onLockPeriod[_addr] = false;
            return onLockPeriod[_addr];
        }else{
            onLockPeriod[_addr] = true;
            return onLockPeriod[_addr];
        }
    }

    // getter functions
    function isMember(address _addr) public view returns(bool){
        return member[_addr];
    }

    modifier onlyMember{
        require(member[msg.sender], "IPWD: Only IPWD member access");
        _;
    }

}