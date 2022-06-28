// contracts/PLToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract PLTToken is ERC20 {
    constructor(uint256 _initialSupply) ERC20("ParkingLotToken", "PLT") {
        _mint(msg.sender, _initialSupply);
    }
}