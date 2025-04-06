# CLATR - Comprehensive Linguistic Analysis of Text for Research

## Overview

CLATR is a modular Python pipeline designed for computational linguistic analysis of textual data, providing detailed insights for linguistic research and analysis. It facilitates preprocessing, multiple specialized linguistic analyses, and comprehensive output management, including aggregation, comparison, clustering, and EDA capabilities.

## Features

- **Preprocessing**: Tokenization and structuring of input text data
- **Sentence/Document Level**: Controlled by `sentence_level` setting
- **Output Options**: Raw tables, aggregated tables, clustering, visualizations
- **Configurable Sections**: Enable/disable individual analyses via settings
  - Graphemes
  - Lexicon
  - Morphology
  - Syntax
  - Phonology
  - Semantics
  - Mechanics

## Directory Structure

```plaintext
project/
├── main.py                  # Entry point
├── utils/                   # Pipeline and output management modules
├── data/                    # Preprocessing and raw input handling
├── analyses/                # Individual analysis functions per linguistic feature
├── input/                   # Input .txt, .docx, .csv, .xlsx, .cha files
├── output/                  # Processed data, visualizations, Excel tables
└── database/                # (Optional) local database storage
```

## How It Works

1. **Initialization**
   - `OutputManager` reads settings and prepares output tables
   - `PipelineManager` sets up selected analysis modules

2. **Preprocessing**
   - Input `.cha` files are parsed, speaker turns cleaned, and sentence/doc-level samples created

3. **Analysis Pipeline**
   - For each selected section:
     - Raw tables are created per granularity (doc/sent)
     - Each sample is processed and results collected
     - Data is written to Excel, optionally clustered and aggregated
     - Visualizations are generated

4. **Output**
   - Excel files saved under `/output/<section>/<granularity>`
   - Clustering, aggregation, and visualizations are optional

## User Configuration (`user_settings.yaml`)

### Input/Output

```yaml
input_dir: input
output_dir: output
database_dir: database
output_label: clatr_data
```

### Processing Flags

```yaml
sentence_level: True         # Use sentence or document granularity
dep_trees: False             # Disable dependency trees
exclude_speakers: [INV]      # Ignore specific speakers in .cha files
```

### Section Selection

Enable or disable specific analyses:

```yaml
sections:
  graphemes: False
  lexicon: True
  morphology: True
  syntax: True
  phonology: True
  semantics: True
  mechanics: False
```

### Aggregation & Group Comparison

```yaml
cluster: True
aggregate: True
compare_groups: False
visualize: True

cohen_d_threshold: 0.8
max_feature_visuals: 5
```

## Installation

### Recommended: Anaconda Navigator Command Line

1. Create a virtual environment:
   ```bash
   conda create --name clatr_env python=3.9
   ```
2. Activate the environment:
   ```bash
   conda activate clatr_env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python src/clatr/main.py
```

## Extending CLATR

To add custom analyses:

1. Add your analysis function in the `analyses/` directory.
2. Update `SECTION_CONFIG` in `PipelineManager.py` to include your analysis function and desired table structures.
3. Enable your analysis in the `user_settings.yaml`.

## Status and Contact

This tool is released as a public **beta** version and is still under active development. While the core functionality is stable and has been used in research contexts, there are aspects of robustness, error handling, and user-friendliness which still want refinement.

I warmly welcome feedback, feature suggestions, or bug reports. Feel free to reach out by:

- Submitting an issue through the GitHub Issues tab

- Emailing me directly at: nsm [at] temple.edu

Thanks for your interest and collaboration!

## Repository Notes

This repository reflects a clean reinitialization of the development history as of April 2025. Earlier commits were removed to:

1. Respect data privacy for sensitive clinical transcript content, even though all `.cha` files used during development were de-identified
2. Eliminate unnecessary storage of output, logs, and database files that were not properly excluded in the previous `.gitignore`

No core functionality or implementation history has been lost, and the full pipeline has been preserved in its final state. All future development will follow a transparent version-controlled workflow.

## Citation

If using CLATR in your research, please cite:

> McCloskey, N., et al. (2025, April). *The RASCAL pipeline: User-friendly and time-saving computational resources for coding and analyzing language samples*. Poster presented at the Aphasia Access Leadership Summit, Pittsburgh, PA.

A copy of the poster will be available through Aphasia Access shared resources.
