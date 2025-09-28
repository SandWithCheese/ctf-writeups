// SPDX-License-Identifier: ISC
pragma solidity ^0.8.0;

struct Account {
    uint128 amount;
    uint128 shares;
}

struct VaultAccount {
    uint128 amount;
    uint128 shares;
}

library Library {
    function toShares(Account memory total, uint256 amount, bool roundUp) internal pure returns (uint256 shares) {
        if (total.amount == 0) {
            shares = amount;
        } else {
            shares = (amount * total.shares) / total.amount;
            if (roundUp && (shares * total.amount) / total.shares < amount) {
                shares = shares + 1;
            }
        }
    }

    function toAmount(Account memory total, uint256 shares, bool roundUp) internal pure returns (uint256 amount) {
        if (total.shares == 0) {
            amount = shares;
        } else {
            amount = (shares * total.amount) / total.shares;
            if (roundUp && (amount * total.shares) / total.amount < shares) {
                amount = amount + 1;
            }
        }
    }
}