// SPDX-License-Identifier: Kiinzu
pragma solidity 0.8.28;

import { UUPSUpgradeable } from "openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol";
import { OwnableUpgradeable } from "openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol";

contract Hope is UUPSUpgradeable, OwnableUpgradeable{

    address private _proxy;

    uint256 private hopeVersion;

    event InitializeHOPEUpgrade(address _newHope, uint256 _fromVersion, uint256 _toVersion);

    function initialize() public initializer{
        __Ownable_init(msg.sender);
        hopeVersion = 1;
    }

    function isHopeAvailable() public pure returns(bool){
        return false;
    }

    function getHopeVersion() public view onlyProxy returns(uint256){
        return _getHopeVersion();
    }

    function _getHopeVersion() internal view onlyProxy returns(uint256) {
        return hopeVersion;
    }

    function _authorizeUpgrade(address _newImplementation) internal override onlyProxy{
        uint256 currentVersion = hopeVersion++;
        uint256 newVersion = hopeVersion;
        emit InitializeHOPEUpgrade(_newImplementation, currentVersion, newVersion);
    }

}