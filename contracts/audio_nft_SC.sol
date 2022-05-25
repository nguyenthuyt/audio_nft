pragma solidity ^0.5.0;

// Using standard for non-fungible tokens. ERC721Full
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// creation of contract.
contract SoundToken is ERC721Full {

    constructor () public ERC721Full("NonFungibleSoundToken", "NFST"){}

    // Art registry set up
    struct Artwork {
        string name;
        string artist;
        uint256 appraisalValue;
    }

    //Define mapping to associate Token ID with a sound NFT
    mapping(uint256 => Artwork) public artCollection;

    // Define an event that logs a new appraisal to the blockchain
    event Appraisal(uint256 token_id, uint256 appraisalValue, string reportURI);

    
    // function allows for the resgistering of audio NFT's
    function registeraNFT(
        address owner, 
        string memory name, 
        string memory artist, 
        uint256 initialAppraisalValue, 
        string memory tokenURI
        ) public returns (uint256){

        // maintains supply total for us.     
        uint256 tokenId = totalSupply();
        // mints tokens based on current supply and owners address.
        _mint(owner, tokenId);
        // associates the tokenID to the address of the file (its URI).
        _setTokenURI(tokenId,tokenURI);
        
        artCollection[tokenId] = Artwork(name, artist, initialAppraisalValue);

        // Function returns tokenID, of current creation.
        return tokenId;
    }

    // Define function that adds a new appraisal value
    function newAppraisal(uint tokenId, uint newAppraisalValue, string memory reportURI) public returns (uint256) {
        //update appraisal value
        artCollection[tokenId].appraisalValue = newAppraisalValue;

        //log new appraisal event to the blockchain
        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return artCollection[tokenId].appraisalValue;

    }


}