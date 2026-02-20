// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./contracts/token/ERC20/utils/SafeERC20.sol";
import "./contracts/token/ERC20/IERC20.sol";
import "./contracts/token/ERC721/ERC721.sol";

contract KittyWarmup is ERC721 {
    using SafeERC20 for IERC20;

    struct Allocation {
        uint24 points;
        bool claimed;
    }

    IERC20 public immutable token;
    address public immutable owner;

    uint256 public constant POINT_TO_TOKEN = 1e18;
    uint24 public constant TARGET_POINTS = 10_000;

    mapping(address => Allocation) public allocations;

    uint256 public nextTokenId;

    event TransferPoints(
        address indexed from,
        address indexed to,
        uint24 amount
    );
    event Claimed(
        address indexed user,
        uint256 amount,
        uint256 firstTokenId,
        uint256 totalNFTsAfter
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor(IERC20 _token) ERC721("KittyNFT", "K-NFT") {
        token = _token;
        owner = msg.sender;
    }

    function seedAllocation(address user, uint24 points) external onlyOwner {
        require(allocations[user].points == 0, "already seeded");
        allocations[user].points = points;
    }

    function transferPoints(address from, address to, uint24 points) external {
        require(msg.sender == from, "only self-managed");

        Allocation memory fromAllocation = allocations[from];
        Allocation memory toAllocation = allocations[to];

        require(fromAllocation.points >= points, "not enough points");

        allocations[from].points = uint24(fromAllocation.points - points);
        allocations[to].points = toAllocation.points + uint24(points);

        emit TransferPoints(from, to, points);
    }

    function claim() external {
        Allocation storage userAlloc = allocations[msg.sender];

        require(!userAlloc.claimed, "already claimed");
        require(userAlloc.points >= TARGET_POINTS, "not enough points");

        uint256 amount = uint256(userAlloc.points) * POINT_TO_TOKEN;

        uint256 mintedTokenId = nextTokenId++;
        _safeMint(msg.sender, mintedTokenId);

        userAlloc.claimed = true;

        token.safeTransfer(msg.sender, amount);

        emit Claimed(msg.sender, amount, mintedTokenId, balanceOf(msg.sender));
    }
}
