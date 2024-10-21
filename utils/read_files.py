import os
import pandas as pd
import docx2txt as dx
from tqdm import tqdm

def read_input_files(input_folder='input/'):
    """
    Read and process input text samples from various formats.

    This function supports multiple input file formats (.cha, .txt, .docx, .csv, .xlsx)
    and extracts text data for linguistic analysis.

    Supported Formats:
    - .cha (ideal format): The filename is used as a label. The file should include
      only one speaker in debulletized format.
    - .txt, .docx: The filename is used as a label. Ensure that the file contains
      only text for analysis.
    - .csv, .xlsx: The tabular format requires two columns: 'label' and 'text'. Each 
      row is treated as an individual text sample.

    Args:
        input_folder (str): The directory containing input files. Defaults to 'input/'.

    Returns:
        dict: A dictionary where each key is the file label and the value is the
        corresponding text from the file.
    """
    samples = {}
    input_folder = os.path.join(os.getcwd(), input_folder)
    input_files = list(os.listdir(input_folder))

    for file_name in tqdm(input_files, desc='Reading Files', total=len(input_files)):
        file_path = os.path.join(input_folder, file_name)
        
        if file_name.endswith('.cha'):
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                sample = ''
                for line in lines:
                    if line.startswith('*'):
                        sample += line[line.index('\t') + 1:]
                samples[file_name] = sample
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
        
        elif file_name.endswith('.txt'):
            try:
                with open(file_path, 'r') as file:
                    samples[file_name] = file.read()
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
        
        elif file_name.endswith('.docx'):
            try:
                samples[file_name] = dx.process(file_path)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
        
        elif file_name.endswith('.xlsx') or file_name.endswith('.csv'):
            try:
                if file_name.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)

                df = df.dropna(subset=['text', 'label'])  # Ensure valid rows
                new_samples = {label: text for label, text in zip(df['label'], df['text'])}
                samples.update(new_samples)

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return samples
