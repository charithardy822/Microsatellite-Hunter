# Microsatellite Hunter 🧬

Microsatellite Hunter is an interactive bioinformatics web application built using Python and Streamlit for detecting microsatellite (SSR) repeat patterns in DNA sequences. The tool allows users to upload FASTA files or paste raw DNA sequences and automatically identifies di-, tri-, and tetra-nucleotide repeats.

## Features

* Upload FASTA files or paste DNA sequences directly
* Detects di-, tri-, and tetra-nucleotide microsatellite repeats
* Adjustable minimum repeat threshold
* Interactive repeat visualization and motif frequency analysis
* Scatter plot showing repeat density across sequence positions
* Downloadable CSV report of detected microsatellites

## Tech Stack

* Python
* Streamlit
* Biopython
* Pandas
* Plotly
* Regex (re)

## Applications

* Microsatellite/SSR analysis
* Genomic sequence exploration
* Bioinformatics education and research
* Repeat pattern visualization

## How to Run

```bash
pip install streamlit biopython pandas plotly
streamlit run microsatellite_hunter.py
```

## Input Supported

* FASTA files (`.fasta`, `.fa`, `.fna`, `.txt`)
* Raw DNA sequences (A, T, G, C)

## Output

* Detected repeat motifs
* Repeat count and genomic positions
* Frequency summary charts
* Downloadable CSV report

Built as part of a DBT–Bioinformatics Centre workshop at SASTRA University.
