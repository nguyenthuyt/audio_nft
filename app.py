###################################################################################
    # Imports
###################################################################################


from io import StringIO
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
import qrcode
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.graph_objects as go
import librosa
import librosa.display
import matplotlib.pyplot as plt
import IPython.display as ipd
import numpy as np
import base64

###################################################################################
    # Background Picture
###################################################################################


bg_ext = 'jpg'

st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{bg_ext};base64,{base64.b64encode(open("Images/image_#1_soundNFT_bg.jpg", "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


###################################################################################
    # Accounts, username, password functionality
###################################################################################

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

###################################################################################
    # Load .env files and connect to web3
###################################################################################

    # Load .env file
    load_dotenv()

    # Connect to web3
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

###################################################################################
    # Contract Helper function:
    # 1. Loads the contract once using cache
    # 2. Connects to the contract using the contract address and ABI
###################################################################################

    # Stop streamlit from auto-refreshing.
    @st.cache(allow_output_mutation=True)

    # Load contract details for deployed contract on injected web3
    def load_contract():
        # load json abi file.
        with open(Path('contracts/compiled/soundToken_abi.json')) as f:
            artwork_abi = json.load(f)

        # Connect to smart deployed smart contract
        contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

        contract = w3.eth.contract(
            address=contract_address,
            abi=artwork_abi
        )

        return contract

    # Load contract information
    contract = load_contract()


###################################################################################
    # Helper functions to pin files and json to Pinata
###################################################################################
    
    # Pinata helper function - pin_artwork
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

###################################################################################
    # Helper functions to create spectrograms
###################################################################################
    def generate_spect(file):
        y, sr = librosa.load(file, offset =0.0, duration=5.0)


        y, sr = librosa.load(file, duration=5)
        fig, ax = plt.subplots(nrows=3, sharex=True)
        librosa.display.waveshow(y, sr=sr, ax=ax[0])
        ax[0].set(title='spectrogram waveplot, mono')
        ax[0].label_outer()

        name = "Spectrogram"
        S = np.abs(librosa.stft(y))
        chroma = librosa.feature.chroma_stft(S=S, sr=sr)
        fig, ax = plt.subplots(nrows=2, sharex=True)
        img1 = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),y_axis='log', x_axis='time', ax=ax[0])
        spect_1 = fig.colorbar(img1, ax=[ax[0]])
        ax[0].label_outer()
        img2 = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
        spect_2 = fig.colorbar( img2, ax=[ax[1]],label = name )

        return spect_1, spect_2

###################################################################################
    # STREAMLIT HOME PAGE
###################################################################################

    # Header
    st.title("Just Audio Non-fungible Tokens")
    st.header("Gotta Collect Em All!")

    # upload image to home screen:
    #img_1 = Image.open("Images/image_#1_soundNFT.jpeg")
    #st.image(img_1, width = 500)


    # Menu Sidebar
    menu = ["Home", "Create A Sound NFT", "Display A Sound NFT", "Display Multiple Sound NFTs", "My JANT Collection","Appraise Sound NFT","Get Appraisals","About"]
    st.sidebar.header("Navigation")
    choice = st.sidebar.selectbox("Menu", menu)
    st.sidebar.write("Pick a selection!")
    
    if choice == "Home":
        st.subheader("Home")
        image_1 = Image.open("images/image_#1_soundNFT.jpeg")
        st.image(image_1, caption="Here hear this sound!")
        st.audio("Sounds/success_horn.wav")

    ################################################################################
    # Option 1 - Create a New Sound NFT
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
    # Option 2 - Display a Sound NFT
    ################################################################################

    elif choice == "Display A Sound NFT":
        st.subheader("Display A Sound NFT")


        accounts = w3.eth.accounts
        selected_address = st.selectbox("Select Account", options=accounts)
        tokens = contract.functions.balanceOf(selected_address).call()
        
        st.write(f"This address owns {tokens} tokens")
            
        token_id = st.selectbox("Sound NFT's", list(range(tokens)))

        token_list = (list(range(tokens)))
            
        
        if st.button('Display'):

            owner = contract.functions.ownerOf(token_id).call()
            st.write(f"Token is registered to {owner}")
            

            token_uri = contract.functions.tokenURI(token_id).call()
            ipfs_hash = token_uri[6:]
            token_url = (f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
            response = requests.get(token_url).json()
            st.write(f"The tokenURI is {token_url}")
            image = response['image']
            name = response['name']
            artist_name = response['artist name']
            value = response['value']
            
                   
            image_url = (f"https://gateway.pinata.cloud/ipfs/{image}")
            st.write(f"The soundURI is {image_url}")
            img = qrcode.make(image_url)
            type(img)
            image_qr = img.save(f"{image}.jpeg")
            #qr_file_image = Image.open("QR.jpeg")
            st.image(f"{image}.jpeg")

            generate_spect(image_url)

            

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.subheader("Name")
                st.write(name)
            with col2:
                st.subheader("Artist")    
                st.write(artist_name)
            with col3:
                st.subheader("Value")
                st.write(f"$ {value}")
            with col4:
                st.subheader("NFT")
                st.audio(image_url, format = "audio/ogg")

            
  
            # gb = GridOptionsBuilder.from_dataframe(df)
            # gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
            # gb.configure_side_bar() #Add a sidebar
            # gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
            # gridOptions = gb.build()

            # grid_response = AgGrid(
            #     df,
            #     gridOptions=gridOptions,
            #     data_return_mode='AS_INPUT', 
            #     update_mode='MODEL_CHANGED', 
            #     fit_columns_on_grid_load=True,
            #     theme='dark', #Add theme color to the table
            #     enable_enterprise_modules=True,
            #     height=350, 
            #     width='100%',
            #     reload_data=False
            # )

            # grid_data = grid_response['data']
            # selected = grid_response['selected_rows'] 
            # dfs = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

            
            

    ################################################################################
    # Option 3 - Display JANT Collection
    ################################################################################
    elif choice == "My JANT Collection":
        st.subheader("My JANT Collection")


        accounts = w3.eth.accounts
        selected_address = st.selectbox("Select Account", options=accounts)
        tokens = contract.functions.balanceOf(selected_address).call()
        token_list = (list(range(tokens)))
        
        
        # Create empty list to populate tokens dataframe
        data = []

        # Set column headers
        col1, col2, col3,col4,col5, col6 = st.columns(6)
        with col1:
            st.subheader("Token")
        with col2:
            st.subheader("Name")
        with col3:
            st.subheader("Artist")
        with col4:
            st.subheader("Value")
        with col5:
            st.subheader("NFT")
        with col6:
            st.subheader("QR Code")

        # Populate data list
        for i in range(tokens):

            token_uri = contract.functions.tokenURI(i).call()
            ipfs_hash = token_uri[6:]
            token_url = (f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
            response = requests.get(token_url).json()
            image = response['image']
            name = response['name']
            artist_name = response['artist name']
            value = response['value']
                   
            image_url = (f"https://gateway.pinata.cloud/ipfs/{image}")

            #Generate QR Code
            img = qrcode.make(image_url)
            type(img)
            image_qr = img.save(f"{image}.jpeg")
        
            # Create table of NFT's
            col1, col2, col3, col4,col5,col6 = st.columns(6)
            with col1:
                #st.subheader("Name")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(f"**{i}**")
            
            with col2:
                #st.subheader("Name")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(f"**{name}**")
            with col3:
                #st.subheader("Artist")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")    
                st.write(f"**{artist_name}**")
            with col4:
                #st.subheader("Value")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(f"**$ {value}**")
            with col5:
                #st.subheader("NFT")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.audio(image_url, format = "audio/ogg")
            with col6:
                st.image(f"{image}.jpeg")

            st.write("------------------------------------------------")

            # Append NFT metadata to data list
            data.append(
                {
                    'name': name,
                    'artist name': artist_name,
                    'value' : value,
                    'sound': image_url
                    
                    }
            )

        # Convert data to dataframe

        df = pd.DataFrame(data)
        
        
    ################################################################################
    # Option 4 - Display Multiple Sound NFTs
    ################################################################################

    elif choice == "Display Multiple Sound NFTs":
        st.subheader("Display Multiple Sound NFTs")


        accounts = w3.eth.accounts
        selected_address = st.selectbox("Select Account", options=accounts)
        # Contract function - calls # of tokens
        tokens = contract.functions.balanceOf(selected_address).call()
        
        st.write(f"This address owns {tokens} tokens")
        
        # Populate data with token list
        token_list = []
        for i in range(tokens):

            token_uri = contract.functions.tokenURI(i).call()
            ipfs_hash = token_uri[6:]
            token_url = (f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
            response = requests.get(token_url).json()
            image = response['image']
            name = response['name']
            artist_name = response['artist name']
            value = response['value']
                   
            image_url = (f"https://gateway.pinata.cloud/ipfs/{image}")

            #img = qrcode.make(image_url)
            #type(img)
            #image_qr = img.save(f"{image}.jpeg")
            #qr_file_image = Image.open("QR.jpeg")
            #st.image(f"{image}.jpeg")

            token_list.append(
                {
                    'token': i,
                    'name': name,
                    'artist name': artist_name,
                    'value' : value,
                    'sound url': image_url
                    
                    }
            )
        
        token_list_df = pd.DataFrame(token_list).set_index(["token"])
        st.write(token_list_df)

        # Select multiple token ids for display    
        token_id = st.multiselect("Sound NFT's", list(range(tokens)))

        
        #token_list = (list(range(tokens)))
            
        
        if st.button('Display'):
            col1, col2, col3,col4 = st.columns(4)
            with col1:
                st.subheader("Name")
            with col2:
                st.subheader("Artist")
            with col3:
                st.subheader("Value")
            with col4:
                st.subheader("Sound")
            st.write("------------------------------------------------")

            for i in token_id:
                owner = contract.functions.ownerOf(i).call()
                #st.write(f"Token is registered to {owner}")
            

                token_uri = contract.functions.tokenURI(i).call()
                ipfs_hash = token_uri[6:]
                token_url = (f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
                response = requests.get(token_url).json()
                #st.write(f"The tokenURI is {token_url}")
                image = response['image']
                name = response['name']
                artist_name = response['artist name']
                value = response['value']
                
                   
                image_url = (f"https://gateway.pinata.cloud/ipfs/{image}")
            #    st.write(f"The soundURI is {image_url}")
            #     img = qrcode.make(image_url)
        #     type(img)
        #     image_qr = img.save(f"{image}.jpeg")
        #     #qr_file_image = Image.open("QR.jpeg")
        #     st.image(f"{image}.jpeg")

            

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                #    st.subheader("Name")
                    st.write(name)
                with col2:
                #    st.subheader("Artist")    
                    st.write(artist_name)
                with col3:
                #    st.subheader("Value")
                    st.write(f"$ {value}")
                with col4:
                #    st.subheader("NFT")
                    st.audio(image_url, format = "audio/ogg")
                st.write("------------------------------------------------")
            
            
    ################################################################################
    # Option 5 - Appraise Sound NFT
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
    # Option 6 - Get Appraisals
    ################################################################################

    elif choice == "Get Appraisals":
        st.subheader("## Get the appraisal report history")
        st.title("Sound NFT Appraisal System")
        st.write("Choose an account to get started")
        accounts = w3.eth.accounts
        address = st.selectbox("Select Account", options=accounts)
        st.markdown("---")

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
    ################################################################################
    # Market Place - Open Sea
    ################################################################################    

    st.sidebar.header("MarketPlace")
    market_choices = ["Pick Endpoint","Assets", "Events", "Rarity"]
    endpoint = st.sidebar.selectbox("OpenSea Enpoints", market_choices)

    if market_choices == "Assets" or market_choices == "Events" or market_choices == "Rarity":
  

        st.title(f"OpenSea API Explorer - {endpoint}")

        if endpoint == 'Events':
            collection = st.sidebar.text_input("Collection")
            asset_contract_address = st.sidebar.text_input("Contract Address")
            token_id = st.sidebar.text_input("Token ID")
            event_type = st.sidebar.selectbox("Event Type", ['offer_entered', 'cancelled', 'bid_withdrawn', 'transfer', 'approve'])
            params = {}
            if collection:
                params['collection_slug'] = collection
            if asset_contract_address:
                params['asset_contract_address'] = asset_contract_address
            if token_id:
                params['token_id'] = token_id
            if event_type:
                params['event_type'] = event_type
        
            r = requests.get('https://testnets-api.opensea.io/api/v1/events', params=params)

            events = r.json()
            
            event_list = []
            for event in events['asset_events']:
                if event_type == 'offer_entered':
                    if event['bid_amount']:
                        bid_amount = Web3.fromWei(int(event['bid_amount']), 'ether')
                    if event['from_account']['user']:
                        bidder = event['from_account']['user']['username']
                    else:
                        bidder = event['from_account']['address']

                    event_list.append([event['created_date'], bidder, float(bid_amount), event['asset']['collection']['name'], event['asset']['token_id']])

            df = pd.DataFrame(event_list, columns=['time', 'bidder', 'bid_amount', 'collection', 'token_id'])
            st.write(df)
            st.write(events)
            
            

        if endpoint == 'Assets':
            st.sidebar.header('Filters')
            owner = st.sidebar.text_input("Owner")
            collection = st.sidebar.text_input("Collection")
            
            params = {'owner': owner}
            if collection:
                params['collection'] = collection

            r = requests.get('https://testnets-api.opensea.io/api/v1/assets')

            assets = r.json()["assets"]
            st.subheader("Raw JSON Data")
            st.write(r.json()["assets"])
    
               
        
        





