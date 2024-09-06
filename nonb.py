import streamlit as st
import re
from pathlib import Path

# Define the motif-finding functions here

def find_direct_repeats(sequence, minDRrep=10, maxDRrep=300, maxDRspacer=100):
    pattern = re.compile(rf'([ATGC]{{{minDRrep},{maxDRrep}}})[ATGC]{{0,{maxDRspacer}}}\1')
    return [(m.start(), m.end(), m.group()) for m in pattern.finditer(sequence)]

# Include other motif-finding functions here (same as the ones you provided)

def process_fasta_content(content):
    sequences = [entry.split('\n', 1) for entry in content.split('>')[1:]]
    results = []
    for header, sequence in sequences:
        sequence = sequence.replace('\n', '')
        motifs = []
        motifs += [(start, end, "Direct Repeat", motif) for start, end, motif in find_direct_repeats(sequence)]
        # Add other motifs in the same way
        
        for start, end, motif_type, *motif in motifs:
            results.append(f">{header.strip()}\nMotif: {motif_type}, Start: {start}, End: {end}, Sequence: {''.join(motif)}\n")
    
    return results

# Streamlit UI
st.title("Motif Finder in DNA Sequences")

# Allow user to either upload a FASTA file or input sequence manually
option = st.radio("Choose how to input sequence:", ("Upload FASTA file", "Enter sequence manually"))

if option == "Upload FASTA file":
    uploaded_file = st.file_uploader("Upload your FASTA file", type=["fasta", "txt"])
    
    if uploaded_file is not None:
        # Process the uploaded file
        content = uploaded_file.read().decode("utf-8")
        results = process_fasta_content(content)
        
        st.write("Motif analysis complete. Results are:")
        for result in results:
            st.text(result)
        st.download_button("Download Results", data='\n'.join(results), file_name="motif_results.txt")

elif option == "Enter sequence manually":
    sequence = st.text_area("Enter your sequence in FASTA format", height=300)
    
    if st.button("Run Motif Finder"):
        if sequence:
            results = process_fasta_content(sequence)
            st.write("Motif analysis complete. Results are:")
            for result in results:
                st.text(result)
        else:
            st.warning("Please enter a valid FASTA sequence.")
