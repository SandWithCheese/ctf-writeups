// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./lib/Account.sol";
import "./lib/ERC20.sol";


contract Vault is ERC20 {
    using Library for Account;

    Account public totalAsset;
    Account public totalBorrow;

    mapping(address => uint256) public userCollateralBalance;
    mapping(address => uint256) public userBorrowShares;
    mapping(address => uint256) public lastBorrow;
    uint256 public totalCollateral;

    ERC20 public immutable asset;
    ERC20 public immutable collateral;

    uint256 public fee;
    uint256 public tier;
    uint256 public minDepositAmount;

    constructor(ERC20 _asset, uint256[] memory params) ERC20("", "") payable {
        asset = _asset;
        collateral = _asset;

        fee = params[0];
        tier = params[1];
        minDepositAmount = params[2] * 10 ** 6;

        _mint(address(this), minDepositAmount);
        totalAsset.shares += uint128(minDepositAmount);
    }

    function totalAssets() public view returns (uint256) {
        return totalAsset.amount;
    }

    function totalShares() public view returns (uint256) {
        return totalAsset.shares;
    }

    function _deposit(Account memory _totalAsset, uint128 _amount, uint128 _shares, address _receiver) internal {
        _totalAsset.amount += _amount;
        _totalAsset.shares += _shares;

        _mint(_receiver, _shares);
        totalAsset = _totalAsset;
        
        asset.transferFrom(msg.sender, address(this), _amount);
    }

    function previewDeposit(uint256 _assets) external view returns (uint256 _sharesReceived) {
        Account memory _totalAsset = totalAsset;
        _sharesReceived = _totalAsset.toShares(_assets, false);
    }

    function deposit(uint256 _amount, address _receiver) external returns (uint256 _sharesReceived) {
        Account memory _totalAsset = totalAsset;

        _sharesReceived = _totalAsset.toShares(_amount, false);

        _deposit(_totalAsset, uint128(_amount), uint128(_sharesReceived), _receiver);
    }

    function previewMint(uint256 _shares) external view returns (uint256 _amount) {
        Account memory _totalAsset = totalAsset;
        _amount = _totalAsset.toAmount(_shares, false);
    }

    function mint(uint256 _shares, address _receiver) external returns (uint256 _amount) {
        Account memory _totalAsset = totalAsset;

        _amount = _totalAsset.toAmount(_shares, false);

        _deposit(_totalAsset, uint128(_amount), uint128(_shares), _receiver);
    }

    function _redeem(
        Account memory _totalAsset,
        uint128 _amountToReturn,
        uint128 _shares,
        address _receiver,
        address _owner
    ) internal {
        if (msg.sender != _owner) {
            uint256 allowed = allowance(_owner, msg.sender);
            if (allowed != type(uint256).max) _approve(_owner, msg.sender, allowed - _shares);
        }

        uint256 _assetsAvailable = _totalAsset.amount;
        if (_assetsAvailable < _amountToReturn) {
            revert ERC20InsufficientBalance(address(this), _assetsAvailable, _amountToReturn);
        }

        _totalAsset.amount -= _amountToReturn;
        _totalAsset.shares -= _shares;

        totalAsset = _totalAsset;
        _burn(_owner, _shares);

        asset.transfer(_receiver, _amountToReturn);
    }

    function previewRedeem(uint256 _shares) external view returns (uint256 _assets) {
        Account memory _totalAsset = totalAsset;
        _assets = _totalAsset.toAmount(_shares, false);
    }

    function redeem(
        uint256 _shares,
        address _receiver,
        address _owner
    ) external returns (uint256 _amountToReturn) {
        Account memory _totalAsset = totalAsset;

        _amountToReturn = _totalAsset.toAmount(_shares, false);

        _redeem(_totalAsset, uint128(_amountToReturn), uint128(_shares), _receiver, _owner);
    }

    function previewWithdraw(uint256 _amount) external view returns (uint256 _sharesToBurn) {
        Account memory _totalAsset = totalAsset;
        _sharesToBurn = _totalAsset.toShares(_amount, true);
    }

    function withdraw(
        uint256 _amount,
        address _receiver,
        address _owner
    ) external returns (uint256 _sharesToBurn) {
        Account memory _totalAsset = totalAsset;

        _sharesToBurn = _totalAsset.toShares(_amount, true);

        _redeem(_totalAsset, uint128(_amount), uint128(_sharesToBurn), _receiver, _owner);
    }

    function _totalAssetAvailable(
        Account memory _totalAsset,
        Account memory _totalBorrow
    ) internal pure returns (uint256) {
        return _totalAsset.amount - _totalBorrow.amount;
    }

}