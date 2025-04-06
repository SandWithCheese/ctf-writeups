pragma solidity ^0.8.0;

// Precompiled certificate library
contract CertificateLibrary {
	address parent;
	mapping(address => uint80) certificateId;

	event EngravedCertificate(address person, uint256 identifier);
	
	function engraveCertificate(address person, uint256 identifier) public {
		certificateId[person] = uint80(identifier);
		emit EngravedCertificate(person, identifier);
	}
}
