import streamlit as st
import requests
import uuid
import json
import os

# Endpoint URL
API_CHAT_ENDPOINT = os.getenv("ENDPOINT_CHAT")
API_REGISTER_ENDPOINT = os.getenv("ENDPOINT_REGISTER")
PASSWORD = os.getenv("PASSWORD_UMA")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    # Get the session state
    st.session_state.key = str(uuid.uuid4())

    # UI to get user input
    user_input = st.text_input('Ingrese su pregunta', '')

    # Button to send the message
    if st.button('Enviar'):
        if user_input:  # Check if there is user input
            # Prepare the payload
            payload = {
                "text": user_input,
                "conversation_id": st.session_state.key
            }
            
            # Make POST request
            response = requests.post(API_CHAT_ENDPOINT, json=payload)
            
            if response.status_code == 200:  # Check if request was successful
                # Extract response data
                data = response.json()
                
                # Display the output received from the API
                st.write(f"Respuesta: {data['output'][0]}")

                data_register = {
                    "question": user_input,
                    "answer": data['output'],
                    "context": 'NONE',
                    "tokens": 0,
                    "price": 0
                }
                payload_register = json.dumps(data_register)
                requests.post(API_REGISTER_ENDPOINT, data=payload_register)
            else:
                st.write(f"Hubo un error en la comunicación. Status code: {response.status_code}")
        else:
            st.write("Ingrese su pregunta")
