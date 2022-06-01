# market place will be on OpenSea.org

import streamlit as st
import requests, json
from web3 import Web3
import pandas as pd

# goal is to connect to opensea and be able to interact with contract and accounts there.

st.sidebar.header("MarketPlace")
market_choices = ["Pick Endpoint","Assets", "Events", "Rarity"]
endpoint = st.sidebar.selectbox("OpenSea Enpoints", market_choices)

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

###################################################

