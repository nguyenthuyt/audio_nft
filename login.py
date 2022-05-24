import streamlit as st
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

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    st.title('Your JANT Account!')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

