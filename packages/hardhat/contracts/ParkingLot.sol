//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./PLTToken.sol";
import "./CarNFT.sol";
// Interface for any contract that wants to support safeTransfers from ERC721 asset contracts.
contract ParkingLot is IERC721Receiver {
    // variables --------------------------------
    PLTToken private _pltToken;
    CarNFT private _carNFT;
    struct ParkedCarNFT {
        uint256 carId;
        uint256 parkedTime;
    }
    uint256 numFreeLots = 5;
    mapping(address => ParkedCarNFT[]) public Parking;
    uint256 costPerMinute = 1000000000000000000; // 1 PLT

    // events ------------------------
    event Retrieved(uint256 feeCharged);
    event Parked(uint256 carId);

    // eslint-disable-next-line
    constructor(PLTToken _plt, CarNFT _car) {
        _pltToken = _plt;
        _carNFT = _car;
    }

    function park(uint256 carId) public {
        require(numFreeLots > 0, "No available space in parking!");
        _carNFT.safeTransferFrom(msg.sender, address(this), carId);
        Parking[msg.sender].push(ParkedCarNFT(carId, block.timestamp));
        numFreeLots --;
        emit Parked(carId);
    }

    function _getFeeCharged(uint256 parkedTime) private view returns(uint256) {
        return ((block.timestamp - parkedTime) / 60) * costPerMinute;
    }

    function retrieve(uint256 carId) public returns (uint256) {
        // find car
        bool isInParking = false;
        uint256 index;
        uint256 length = Parking[msg.sender].length;
        for(uint256 i=0; i<length; i++){
            uint256 localCarId = Parking[msg.sender][i].carId;
            if(localCarId == carId){
                isInParking = true;
                index = i;
                break;
            }
        }
        if(isInParking == false){ revert("Car is not in parking!");}
        // feeCharged
        uint256 feeCharged = _getFeeCharged(Parking[msg.sender][index].parkedTime);
        if (_pltToken.balanceOf(msg.sender) < feeCharged){
            revert("You don't have enough PLT to retrieve ur carNFT!");
        }
        // pop car and withdraw PLT
        Parking[msg.sender][index] = Parking[msg.sender][length-1];
        Parking[msg.sender].pop();
        _carNFT.safeTransferFrom(address(this), msg.sender, carId);
        _pltToken.transferFrom(msg.sender, address(this), feeCharged);
        numFreeLots ++;

        emit Retrieved(feeCharged);

        return feeCharged;
    }

    function parkedCars(address user) public view returns (uint256[] memory) {
        uint256[] memory userCars = new uint256[](Parking[user].length);
        for(uint256 i=0; i<Parking[user].length; i++){
            userCars[i] = Parking[user][i].carId;
        }
        return userCars;
    }

    function availableLots() public view returns (uint256) {
        return numFreeLots;
    }

    //    https://ethereum.stackexchange.com/questions/48796/whats-the-point-of-erc721receiver-sol-and-erc721holder-sol-in-openzeppelins-im
    function onERC721Received(
        address,
        address,
        uint256,
        bytes memory
    ) public virtual override returns (bytes4) {
        return this.onERC721Received.selector;
    }

    function parkedCarsCount(address user) public view returns (uint256) {
        return Parking[user].length;
    }

    struct ParkedCarInfo {
        uint256 carId;
        uint256 feeCharged;
    }

    function ping() public view returns (uint256) {
        return block.timestamp;
    }

    function parkedCarOfOwnerByIndex(address user, uint256 _id) public view returns (ParkedCarInfo memory) {
        require(_id < Parking[user].length);
        uint256 feeCharged = _getFeeCharged(Parking[user][_id].parkedTime);
        return ParkedCarInfo(
            Parking[user][_id].carId, feeCharged
        );
    }
}
