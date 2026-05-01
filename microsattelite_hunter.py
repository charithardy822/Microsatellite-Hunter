# microsatellite_hunter.py
import streamlit as st
from Bio import SeqIO
import pandas as pd
import re
import plotly.express as px
import io

st.set_page_config(page_title=" Microsatellite Hunter", layout="wide")
st.title("Microsatellite Hunter — DNA Repeat Pattern Finder")
st.markdown("Upload a DNA FASTA file **or** paste your sequence below to detect di-, tri-, and tetra-nucleotide repeat patterns.")

# Input options
uploaded = st.file_uploader("📂 Upload FASTA file", type=["fasta", "fa", "txt", "fna"])
st.markdown("**OR**")
pasted_seq = st.text_area(" Paste DNA sequence here (A, T, G, C only)🧬", height=150)

# Function to find microsatellites
def find_repeats(sequence, min_repeat=3):
    sequence = sequence.upper().replace("\n", "").replace(" ", "")
    results = []
    for size in [2, 3, 4]:  # motif sizes
        for i in range(len(sequence) - size):
            motif = sequence[i:i+size]
            if "N" in motif:
                continue
            pattern = f"({motif}){{{min_repeat},}}"
            for match in re.finditer(pattern, sequence):
                start = match.start() + 1
                end = match.end()
                repeat_count = int((end - start + 1) / size)
                results.append({
                    "Motif": motif,
                    "Repeat Count": repeat_count,
                    "Start": start,
                    "End": end
                })
    return pd.DataFrame(results)

# Load sequence (either upload or paste)
sequence = None
if uploaded:
    try:
        # Convert binary file to text stream
        stringio = io.StringIO(uploaded.getvalue().decode("utf-8"))
        record = next(SeqIO.parse(stringio, "fasta"))
        sequence = str(record.seq)
        st.success(f"✅ Sequence loaded from file! ({len(sequence)} bases)")
    except Exception as e:
        st.error(f"Error reading FASTA: {e}")
elif pasted_seq.strip():
    sequence = pasted_seq.strip()
    st.success(f"✅ Sequence pasted successfully! ({len(sequence)} bases)")
else:
    st.info("Upload a FASTA file **or** paste a DNA sequence to begin.")

# Main analysis
if sequence:
    min_rep = st.slider("Minimum repeat count threshold", 3, 10, 4)

    if st.button("Find Microsatellites"):
        with st.spinner("Scanning sequence for repeats..."):
            df = find_repeats(sequence, min_repeat=min_rep)

        if not df.empty:
            st.subheader("Detected Microsatellites")
            st.dataframe(df, use_container_width=True, height=300)

            # Summary chart
            motif_summary = (
                df.groupby("Motif").size()
                .reset_index(name="Occurrences")
                .sort_values(by="Occurrences", ascending=False)
            )
            st.subheader("Motif Frequency Summary")
            st.bar_chart(motif_summary.set_index("Motif"))

            # Scatter plot
            st.subheader("Repeat Density Along Sequence")
            fig = px.scatter(
                df, x="Start", y="Repeat Count", color="Motif",
                title="Microsatellite Distribution",
                labels={"Start": "Position (bp)", "Repeat Count": "Repeat Length"}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Download
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download Repeat Report", csv, "microsatellites.csv", "text/csv")
        else:
            st.warning("⚠️ No significant repeats found with the selected threshold.")
