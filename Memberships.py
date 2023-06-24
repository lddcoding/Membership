import streamlit as st
import base64
import stripe
from deta import Deta
from streamlit.components.v1 import html

# Initialize the connection to the detabase and stripe for payments
detakey = 'b0gyysefask_b6YH6nraDHXYtt7dG7fb5boNjqQDPPtS'
deta = Deta(detakey)
db = deta.Base("ticketscrappertest1")
stripe.api_key = 'sk_test_51NKnf0B82uB4EE73dTW5Hcyrd1WkYVLAhWhRF4S3W51cy1FKp8BXCXFn2kVjWBAfJv0EfnRJj6wCcm1eKulcwgb200iDLos5GF'

def create_checkout_session(price_id, email):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://yourwebsite.com/success',
        cancel_url='https://yourwebsite.com/cancel',
        customer_email=email
    )
    return session

def check_value_exists(column_name, value):
    # Query the database for rows with the specified value in the column
    query = db.fetch({column_name : value})
    
    # Check if any rows are returned
    if len(query.items) > 0:
        return True #value does exist
    else:
        return False #value does not exist

def find_dictionary_index(dictionaries, email):
    for index, dictionary in enumerate(dictionaries):
        if dictionary.get('email') == email:
            return index
    return -1

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)


# Extract the encoded email and password from the URL parameters
encoded_email = st.experimental_get_query_params().get("email", [""])[0]


# Decode the email and password using Base64
email = base64.b64decode(encoded_email).decode()

if check_value_exists("email", email) == True:

    # Get the specific user information from the database
    content = db.fetch().items
    index = find_dictionary_index(content, email)
    key_db = content[index]['key']
    user_data = db.get(key_db)

    st.title("Memberships")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Monthly Membership:')
        st.write('Get access for ...')
        session_monthly = create_checkout_session('price_1NLE87B82uB4EE73r80KE89a', user_data['email'])
        st.button('Open link', on_click=open_page(session_monthly.url), key='1')
            
        


    with col2:
        st.subheader('Annualy Membership:')
        st.write('Get access for ...')
        session_annualy = create_checkout_session('price_1NLE8KB82uB4EE73Tph9Qghz', user_data['email'])
        st.button('Open link', on_click=open_page(session_annualy.url), key='2')
        

else:
    st.error("The email wasn't found in the database")
