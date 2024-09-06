import streamlit as st

# Streamlit Title
st.title("Simple DNA Sequence Display")

# Input text area for the user to input their DNA sequence
sequence = st.text_area("Enter your DNA sequence", height=200)

# Button to trigger the display
if st.button("Display Sequence"):
    if sequence:
        st.write("Here is your DNA sequence:")
        st.text(sequence)
    else:
        st.warning("Please enter a valid DNA sequence.")
