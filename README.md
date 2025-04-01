# CLATR - Computational Linguistic Analysis of Text for Research

## Overview

CLATR is a modular Python pipeline designed for computational linguistic analysis of textual data, providing detailed insights for linguistic research and analysis. It facilitates preprocessing, multiple specialized linguistic analyses, and comprehensive output management, including aggregation, comparison, clustering, and visualization capabilities.

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
output_label: test_clustermap
```

### Processing Flags

```yaml
sentence_level: True         # Use sentence or document granularity
dep_trees: False             # Disable dependency trees
exclude_speakers: [INV]      # Ignore specific speakers
```

### Section Selection

Enable or disable specific analyses:

```yaml
sections:
  graphemes: False
  lexicon: True
  morphology: False
  syntax: False
  phonology: False
  semantics: False
  mechanics: False
```

### Aggregation & Group Comparison

```yaml
cluster: False
aggregate: False
compare_groups: False
visualize: True

cohen_d_threshold: 0.8
max_feature_visuals: 5
```

## Usage

```bash
python src/clatr/main.py
```

## Dependencies

Install with:

```bash
pip install -r requirements.txt
```

## Notes

- Input files should follow CHAT (.cha) format
- Results will be exported as Excel spreadsheets
- Customize the workflow through `user_settings.yaml`

## License

MIT License

## Authors

Developed by Nick McCloskey in the Speech, Language, and Brain lab at Temple University.

## Extending CLATR

To add custom analyses:

1. Add your analysis function in the `analyses/` directory.
2. Update `SECTION_CONFIG` in `PipelineManager.py` to include your analysis function and desired table structures.
3. Enable your analysis in the `user_settings.yaml`.

## Contributing

Contributions and feedback are welcome. Please submit a pull request or open an issue for discussion.

