pragma solidity ^0.5.0;

// Using standard for non-fungible tokens. ERC721Full
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// creation of contract.
contract SoundToken is ERC721Full {

    constructor () public ERC721Full("NonFungibleSoundToken", "NFST"){}

    // function allows for the resgistering of audio NFT's
    function registeraNFT(address owner, string memory tokenURI) public returns (uint256){

        // maintains supply total for us.     
        uint256 tokenId = totalSupply();
        // mints tokens based on current supply and owners address.
        _mint(owner, tokenId);
        // associates the tokenID to the address of the file (its URI).
        _setTokenURI(tokenId,tokenURI);

        // Function returns tokenID, of current creation.
        return tokenId;

    }


}