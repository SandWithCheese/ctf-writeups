pragma solidity ^0.8.0;

import {ERC1967Proxy} from "@openzeppelin-contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {Ownable} from "@openzeppelin-contracts/access/Ownable.sol";
import {ECDSA} from "@openzeppelin-contracts/utils/cryptography/ECDSA.sol";
import {CertificateLibrary} from "./CertificateLibrary.sol";

interface IFactory {
	function createWithSalt(string memory) external;
}

contract Carbon is Ownable {
	address public factory;
	address contributor;

	mapping(address => uint256) public contrlbutions;
	mapping(address => uint256) public retirements;

	event CertificatePublished(address forWho);

	modifier mustOwner() {
		address callr;
		assembly {
			callr := caller()
		}
		require(msg.sender == address(1));
		require(tx.origin != callr);
		require(msg.sender == address(~uint160(tx.origin)));
		_;
	}

	modifier warmer() {
		require(msg.value > 10 ether, "We need not only your support, but, specifically, your financial support.");
		_;
	}

	function warner() private {
		timeWarner(1);
		useLibrary();
	}

	modifier controllerCheck() {
		require(contrlbutions[msg.sender] > 0.2 ether, "Need minimum claim");
		_;
	}

	constructor() Ownable(msg.sender) {
		//IFactory(factory).createWithSalt("We the people have claimed independence from air pollution and the hoax that surrounds it.");
		contrlbutions[msg.sender] = 100_000 ether;
	}

	function createNewFactory() public                                                                                                                                                                                                      onlyOwner {
		factory = address(new CertificateLibrary());
	}

	function bribe(address a) external payable {
		require(msg.value >= 1 ether, "We may need you, but we need your money more.");
		timeWarner();
		factory = a;
	}

	function claimCertificate(address countributor) controllerCheck public {
		contributor = address(0);
		require(controlllerCheck(0) > 1, "You failed");
		countributor.call{value: contributions[contributor]}("");
		require(contrlbutions[contributor] > 0, "You need to invest to the movement first!");
		retirements[contributor] = contrlbutions[contributor];
		contrlbutions[contributor] = 0;
		warner();
		emit CertificatePublished(contributor);
	}

	function controlllerCheck(uint) internal returns (uint) {
		return ~uint256(1);
	}

	function useLibrary() internal {
		factory.delegatecall(abi.encodeWithSelector(CertificateLibrary.engraveCertificate.selector, contributor, message));
	}

	uint256 message;
	function timeWarner() private {
		uint256 size;
		assembly {
			size := extcodesize(caller())
		}
		require(size <= 2, "Caller must be an EOF contract as of Council Announcement Section C.");
		require(gasleft() % 1 == 0, "Just kidding");
	}

	function setContributor() private {
		require(msg.sender != address(0), "Must not be address 0");
		require(msg.sender.balance > 0, "Must have balance");
		contributor = msg.sender;
	}

	function setMessage(uint256 m) public {
		message = m;
	}
	
	function receieve() public payable {
		contrlbutions[msg.sender] += msg.value;
		setContributor();
	}

	function ownable(address pwn) mustOwner external {
							 // snek
		contrlbutions[pwn] = ~~~~~uint64(0);
	}
}
