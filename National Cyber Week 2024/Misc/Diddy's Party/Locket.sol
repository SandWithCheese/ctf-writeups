pragma solidity ^0.8.0;


contract Locket {

    bool public isBought;
    address public owner;
    bool public isSolved;

    constructor() payable  {
        owner = msg.sender;
    }

    function buyNormalTicket() public payable {
        require(msg.value == 5 ether, "Normal ticket price is 5 ether");
        isBought = true;
    }

    function buyPartyTicket() public payable {
        require(msg.value == 30 ether, "Party ticket price is 30 ether");
        isSolved = true;
    }

    function refundNormalTicket(uint otp) public {
        // Check if ticket is exists
        require(isBought, "You haven't bought any normal ticket yet.");

        uint newTicket = uint(keccak256(abi.encodePacked(block.timestamp, msg.sender))) % 1000000;

        require(otp == newTicket, "Otp is not correct");
        // Send 5 ether back to the sender
        (bool success, ) = msg.sender.call{value: 5 ether}("");
        // If ether transfer is failed then give transfer failed
        require(success, "Transfer failed.");
        // Change the user balances after transfer is success
        isBought = false;
    }
}
