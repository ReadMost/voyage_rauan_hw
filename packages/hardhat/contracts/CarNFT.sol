// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts v4.4.1 (token/ERC721/extensions/ERC721Enumerable.sol)

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

import "./PLTToken.sol";
//https://ethereum.stackexchange.com/questions/97163/undeclared-identifier-settokenuri-in-erc721
contract CarNFT is ERC721URIStorage, ERC721Enumerable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    PLTToken private _pltToken;
    uint256 private _amount = 100000000000000000000; // 100 PLT

    event Created(uint256 carId);

    constructor(PLTToken _plt) ERC721("CarNFT", "CNFT"){
        _pltToken = _plt;
    }

    function createCar(
        string memory imgURL
    )
    public
    returns (uint256) {
        if (_pltToken.balanceOf(msg.sender) < _amount ){
            revert("Insufficient balance");
        }
        _tokenIds.increment();

        uint256 newCarId = _tokenIds.current();
        _safeMint(msg.sender, newCarId);
        _setTokenURI(newCarId, imgURL);

        _pltToken.transferFrom(msg.sender, address(this), _amount);
        emit Created(newCarId);
        return newCarId;
    }






//    methods which have several implementations
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    )
    internal
    virtual
    override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function _burn(
        uint256 tokenId
    ) internal
    override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

     function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}