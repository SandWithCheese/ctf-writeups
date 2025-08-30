// SPDX-License-Identifier: Kiinzu
pragma solidity 0.8.28;

import { Hope } from "./Hope.sol";
import { HopeBeacon } from "./HopeBeacon.sol";


contract Setup{
    Hope public immutable hope;
    HopeBeacon public immutable HB;

    constructor() payable {
        hope = new Hope();

        bytes memory initializationCall = abi.encodeCall(hope.initialize, ());
        HB = new HopeBeacon(address(hope), initializationCall);
    }

    function isSolved() external returns(bool){
        bytes memory testIfSolve = abi.encodeCall(hope.isHopeAvailable, ());
        (bool success, bytes memory rawData) = address(HB).call(testIfSolve);
        require(success);
        return abi.decode(rawData, (bool));
    }
    
}
