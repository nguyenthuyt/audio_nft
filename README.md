# Just Audio Non-Fungible Tokens (JANT)

The purpose of JANT is to host a streamlit web app to allow users to register, collect, and view sound NFT's.
    
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
![SAMPLE env](Sample_env.PNG)






## Streamlit Demo

In the terminal, Streamlit run app.py
![Demo video](Images/TBD.mov)



## Conclusion and Next Steps


---

## Contributors

This project was created as part of the Rice Fintech Bootcamp 2022 Program by:

Jas Pinglia - https://github.com/jpinglia ; https://www.linkedin.com/in/JPinglia

Angela Richter - https://github.com/angie0920 ; https://www.linkedin.com/in/angela-richter-55017233

Neil Mendelow - https://github.com/nmendelow ; https://www.linkedin.com/in/neil-mendelow/ 

Thuy Nguyen - https://github.com/nguyenthuyt ; https://linkedin.com/in/nguyenthuyt


---

## License

MIT




