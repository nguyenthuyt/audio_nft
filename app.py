#imports
import os
import json
import requests
import pandas as pd
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
from multiprocessing import AuthenticationError
import streamlit_authenticator as stauth

#Accounts, username, password functionality
names = ['Angela Richter','Jas Pinglia', 'Thuy Nguyen', 'Neil Mendelow']
usernames = ['arich','jpag', 'tweezy4sheezy', 'nmannilow']
passwords = ['123','1234', '12345', '123456']
wallet_addresses = ['x', 'b', 'c', 'a']

hashed_passwords = stauth.Hasher(passwords).generate()


authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=300)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status == False:
    st.error('Username/password is incorrect')        
elif authentication_status == None:
    st.warning('Please enter your username and password')  
elif authentication_status:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    st.title('Your JANT Account!')

    # load .env file
    load_dotenv()

    # connect to web3
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

    ################################################################################
    # Contract Helper function:
    # 1. Loads the contract once using cache
    # 2. Connects to the contract using the contract address and ABI
    ################################################################################

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


    ################################################################################
    # Helper functions to pin files and json to Pinata
    ################################################################################


    def pin_artwork(artwork_name, artwork_file, value, artist_name):
        # Pin the file to IPFS with Pinata
        ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

        # Build a token metadata file for the artwork
        token_json = {
            "name": artwork_name,
            "artist name": artist_name,
            "image": ipfs_file_hash,
            "value": value
        }
        json_data = convert_data_to_json(token_json)

        # Pin the json to IPFS with Pinata
        json_ipfs_hash = pin_json_to_ipfs(json_data)

        return json_ipfs_hash


    def pin_appraisal_report(report_content):
        json_report = convert_data_to_json(report_content)
        report_ipfs_hash = pin_json_to_ipfs(json_report)
        return report_ipfs_hash


    #st.title("Sound NFT Appraisal System")
    #st.write("Choose an account to get started")
    accounts = w3.eth.accounts
    #address = st.selectbox("Select Account", options=accounts)
    st.markdown("---")


    # accounts connected to injected web3
    st.title("Sound NFTs - Gotta Collect Em All")
    st.header("Register A Sound as NFT!!")

    # upload image to home screen:
    img_1 = Image.open("Images/image_#1_soundNFT.jpeg")
    st.image(img_1, width = 700)

    menu = ["Home", "Create A Sound NFT", "About", "Display A Sound NFT", "Appraise Sound NFT","Get Appraisals"]
    st.sidebar.header("Navigation")
    choice = st.sidebar.selectbox("", menu)

    st.sidebar.write("Pick a selection!")

    st.button("Get Started")


    if choice == "home":
        st.subheader("home")
        image_1 = Image.open("images/image_#1_soundNFT.jpeg")
        st.image(image_1, caption="Here hear this sound!")

    ################################################################################
    # Create a New Sound NFT
    ################################################################################

    elif choice == "Create A Sound NFT":
        st.subheader("Create A Sound NFT")

        artwork_name = st.text_input("Enter the name of the sound NFT")
        artist_name = st.text_input("Enter the artist name")
        initial_appraisal_value = st.text_input("Enter the initial appraisal amount")

        sound_file = st.file_uploader("Upload Sound", type = ["mp3", "mp4", "wav","m4a"])
        

        if sound_file is not None:
            st.write(type(sound_file))
            st.success("Successful File Upload")
            
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


            
            # sound is registered. 
            if st.button("Register Sound"):
                artwork_ipfs_hash = pin_artwork(artwork_name, sound_file, initial_appraisal_value, artist_name)
                artwork_uri = f"ipfs://{artwork_ipfs_hash}"
                hasher = artwork_uri
                tx_hash = contract.functions.registeraNFT(
                    address,
                    artwork_name,
                    artist_name,
                    int(initial_appraisal_value),
                    artwork_uri
                ).transact({'from': address, 'gas': 1000000})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                st.write("Transaction receipt mined:")
                st.write(dict(receipt))
                st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
                st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
            st.markdown("---")


        

    ################################################################################
    # Display a Sound NFT
    ################################################################################

    elif choice == "Display A Sound NFT":
        st.subheader("Display A Sound NFT")


        accounts = w3.eth.accounts
        selected_address = st.selectbox("Select Account", options=accounts)
        tokens = contract.functions.balanceOf(selected_address).call()
        
        st.write(f"This address owns {tokens} tokens")
            
        token_id = st.selectbox("Sound NFT's", list(range(tokens)))

        

        if st.button('Display'):

            owner = contract.functions.ownerOf(token_id).call()
            st.write(f"Token is registered to {owner}")

            token_uri = contract.functions.tokenURI(token_id).call()
            ipfs_hash = token_uri[6:]
            token_url = (f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
            response = requests.get(token_url).json()
            image = response['image']
                   
            image_url = (f"https://gateway.pinata.cloud/ipfs/{image}")

            st.write(f"The tokenURI is {token_url}")
            
            st.audio(image_url, format = "audio/ogg")

    ################################################################################
    # Appraise Sound NFT
    ################################################################################

    elif choice == "Appraise Sound NFT":
        st.subheader("## Appraise Sound NFT")
        tokens = contract.functions.totalSupply().call()
        token_id = st.selectbox("Choose an Sound Token ID", list(range(tokens)))
        new_appraisal_value = st.text_input("Enter the new appraisal amount")
        report_uri = st.text_area("Enter notes about the appraisal")
        if st.button("Appraise Sound NFT"):

            # Use the token_id and the report_uri to record the appraisal
            tx_hash = contract.functions.newAppraisal(
                token_id,
                int(new_appraisal_value),
                report_uri
            ).transact({"from": w3.eth.accounts[0]})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
        st.markdown("---")

    ################################################################################
    # Get Appraisals
    ################################################################################

    elif choice == "Get Appraisals":
        st.subheader("## Get the appraisal report history")
        art_token_id = st.number_input("Sound Token ID", value=0, step=1)
        if st.button("Get Appraisal Reports"):
            appraisal_filter = contract.events.Appraisal.createFilter(
                fromBlock=0,
                argument_filters={"tokenId": art_token_id}
            )
            appraisals = appraisal_filter.get_all_entries()
            if appraisals:
                for appraisal in appraisals:
                    report_dictionary = dict(appraisal)
                    st.markdown("### Appraisal Report Event Log")
                    st.write(report_dictionary)
                    st.markdown("### Appraisal Report Details")
                    st.write(report_dictionary["args"])
            else:
                st.write("This sound NFT has no new appraisals")
 




