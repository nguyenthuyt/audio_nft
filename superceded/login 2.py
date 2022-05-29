import streamlit as st
import streamlit_authenticator as stauth
import plotly.graph_objects as go
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode



#page title
st.title('Just Audio NfT')

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
    st.title('Your JANT Account!')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


if authentication_status == True:
    
    interactive = st.container()
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