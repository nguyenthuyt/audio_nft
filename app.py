#imports
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

# load .env file
load_dotenv()

# connect to web3
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# stop streamlit from auto-refreshing.
@st.cache(allow_output_mutation=True)

# load contract details for deployed contract on injected web3
def load_contract():
    # load json abi file.
    with open(Path('contracts/compiled/soundToken_abi.json')) as f:
        artwork_abi = json.load(f)

    # connect to smart deployed smart contract
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

# load contract information
contract = load_contract()

# accounts connected to injected web3
st.title("Sound NFTs - Gotta Collect Em All")
st.header("Register A Sound as NFT!!")

# upload image to home screen:
img_1 = Image.open("Images/image_#1_soundNFT.jpeg")
st.image(img_1, width = 700)

menu = ["Home", "Create A Sound NFT", "About"]
st.sidebar.header("Navigation")
choice = st.sidebar.selectbox("", menu)

st.sidebar.write("Pick a selection!")

st.button("Get Started")

if choice == "home":
    st.subheader("home")
    image_1 = Image.open("images/image_#1_soundNFT.jpeg")
    st.image(image_1, caption="Here hear this sound!")


elif choice == "Create A Sound NFT":
    st.subheader("Create A Sound NFT")
    sound_file = st.file_uploader("Upload Sound", type = ["mp3", "mp4", "wav"])
    
    if sound_file is not None:
        st.write(type(sound_file))
        st.success("Successfull File Upload")
        
        st.write("File Preview")
        #st.write(dir(sound_file))
        #file_details = {"filename": sound_file.name, "filetype": sound_file.type, "filesize": sound_file.size, "file directory": sound_file.__dict__}
        #st.write(file_details)
        st.write(sound_file.__dict__)
        st.audio(sound_file, format = "audio/ogg")

        sound_path = sound_file.name
        #sound path for URI
        st.write(sound_path)
        
        
        #linked ether accounts
        accounts = w3.eth.accounts
        address = st.selectbox("Select Sound Owner", options=accounts)

        sound_uri = sound_path

        # sound is registered. 
        if st.button("Register Sound"):
            # need to UPDATE GAS FUNCTIONAITY
            tx_hash = contract.functions.registeraNFT(address, sound_uri).transact({
                "from": address,
                "gas": 1000000
            })
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write("Transaction receipt mined:")
            st.write(dict(receipt))
    






