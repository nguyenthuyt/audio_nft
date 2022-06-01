# Just Audio Non-Fungible Tokens (JANT)

The purpose of this challenge is to use Solidity to launch a crowdsale contract that will allow people who are moving to Mars to convert their earthling money to KaseiCoin. You will create a fungible token that is ERC-20 compliant and that will be minted by using a Crowdsale contract from the OpenZeppelin Solidity library.
    
---

## Technologies

This analysis leverages Solidity (pragma ^0.5.5) and utilizes Remix IDE, Metamask, and Ganache to build and test smart contracts.

---

## Installation Guide

Install the Metamask browser extension and Ganache before running this program.

---

## Usage
The challenge is hosted on the following GitHub repository at: https://github.com/nguyenthuyt/audio_nft   

### **Run instructions:**
To run this project, simply clone the repository or download the files. Open a Remix IDE web browser instance and navigate to the directory that contains the following files:
**app.py**


and deploy the following contract:
**audio_nft_sc**

## Remix IDE Deployment
To compile and deploy the file using the following steps:

- Select the Injected Web3 environment
- From the Contract menu, select the audio_nft_sc contract
- Compile and deploy the contract

![Remix Compile](Evaluation_Evidence/KaseiCoinCrowdsaleDeployer.PNG)

- An instance of Metamask will appear asking to confirm the transaction. Click confirm to proceed.



## Populate .env file

- Navigate to SAMPLE.env and populate with the deployed contract address from Remix IDE. Also, fill in Pinata API information and Ganache RPC URL.
![Remix Minted Tokens]("""".PNG)


- To view the total wei raised from the crowdsale, navigate to the KaseiCoinCrowdsale contract and click on 'weiRaised'
![Remix Wei Raised](.PNG)



## Streamlit Demo

In the terminal, Streamlit run app.py
![Remix KaseiCoin Token Contract](Evaluation_Evidence/compiled_KaseiCoin.PNG)



## Conclusion and Next Steps


---

## Contributors

This project was created as part of the Rice Fintech Bootcamp 2022 Program by:

Jas Pinglia - https://github.com/jpinglia ; https://www.linkedin.com/in/JPinglia/ Angela Richter - https://github.com/angie0920 Neil Mendelow - https://github.com/nmendelow ; https://www.linkedin.com/in/neil-mendelow/ Thuy Nguyen - https://github.com/nguyenthuyt


---

## License

MIT




# audio_nft
Audio NFT Marketplace
