import streamlit as st
import streamlit_authenticator as stauth
import plotly.graph_objects as go
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import io
from PIL import Image
import base64
#background picture

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

#Accounts, username, password functionality
names = ['Angela Richter','Jas Pinglia', 'Thuy Nguyen', 'Neil Mendelow']
usernames = ['arich','jpag', 'tweezy4sheezy', 'nmannilow']
passwords = ['123','1234', '12345', '123456']
wallet_addresses = ['x', 'b', 'c', 'a']

hashed_passwords = stauth.Hasher(passwords).generate()


authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=300)

name, authentication_status, username = authenticator.login('Login','main')


if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    st.header('Your JANT Account!')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


if authentication_status == True:
    
    audio_file1 = open('./Sounds/covidcough.wav', 'rb') #enter the filename with filepath

    audio_bytes1 = audio_file1.read() #reading the file

    st.audio(audio_bytes1, format='audio/wav') #displaying the audio
    category = st.multiselect(
     'Select Categories',
     ['Green', 'Yellow', 'Red', 'Blue'])

    if category is not None:
        st.write('You selected:', category)
    #NFT Dataframe
    data = {'Name': ['NFT1', 'NFT2', 'NFT3', 'NFT4'],
        'Category': ['test', 'cat', 'dog', 'baby'],
        'Value': [10, 500, 400, 200]}

    df = pd.DataFrame(data)
  
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=True,
        theme='dark', #Add theme color to the table
        enable_enterprise_modules=True,
        height=350, 
        width='100%',
        reload_data=False
    )

    grid_data = grid_response['data']
    selected = grid_response['selected_rows'] 
    dfs = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
    





##code from https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031