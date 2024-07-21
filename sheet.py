from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd
import re
import os
import pymupdf
import pdfplumber
import csv





'''extract the tables from pdf file'''
def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract tables from the page
            page_tables = page.extract_tables()
            print(len(page_tables))
            for table_index, table in enumerate(page_tables):
                tables.append({
                    "page_num": page_num + 1,  # 1-based page number
                    "table_index": table_index + 1,  # 1-based table index
                    "table": table
                })
    return tables

def save_tables_to_csv(tables, base_csv_path):
    for table_info in tables:
        csv_path = f"{base_csv_path}_page{table_info['page_num']}_table{table_info['table_index']}.csv"
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for row in table_info['table']:
                writer.writerow(row)
        print(f"Table {table_info['table_index']} from page {table_info['page_num']} saved to {csv_path}")

pdf_path = "./assignment1/infos/fact-sheet.pdf"
base_csv_path = "./sheet/"
tables = extract_tables_from_pdf(pdf_path)
save_tables_to_csv(tables, base_csv_path)
print('table extraction done')




'''necessary functions for sheet analysis'''
# Load the pre-trained transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Replacement dictionary
replacements = {
    "YoY": "year-on-year",
    "QoQ": "quarter-on-quarter",
    "CC": "constant currency",
    "&": "and",
    "($)": "(in doller)"
}

#specific functions designed for tables 1 to 4
def extract_text_from_csv(file_path):
    # extract text 
    df = pd.read_csv(file_path)
    txt= []
    for index, row in df.iterrows():
        if row.values:
            row_text = ' '.join(map(str, row.values))
            txt.append(row_text)
    final_txt = " ".join(txt)
    
    # Remove 'nan'
    final_txt = re.sub(r'\bnan\b', '', final_txt, flags=re.IGNORECASE)
    
    # Replace abbreviation terms based on the dictionary
    for key, value in replacements.items():
        final_txt = final_txt.replace(key, value)
    
    return final_txt

#functions to split text of earning calls 
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
def split_sentences(text):
    sentence_endings = re.compile(r'(?<!\d)\. (?=\w)|(?<!\d)\.\n')
    sentences = sentence_endings.split(text)
    return sentences
    



'''the clean earning call text (with which we would like to connect the tables)'''
# the compact text
texts=[]
directory_path = "./sheet/texts"
filenames = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
for filename in sorted(filenames):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            texts.append(file.read())
combined_text = "\n\n".join(texts)
sentences = split_sentences(combined_text)
sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

# the sector text
sector_texts=[]
file_path = "./sheet/texts/sector.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    sector_texts.append(file.read())
sector_combined_text = "\n\n".join(sector_texts)
sector_sentences = split_sentences(sector_combined_text)
sector_sentence_embeddings = model.encode(sector_sentences, convert_to_tensor=True)

# the region text
region_texts=[]
file_path = "./sheet/texts/region.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    region_texts.append(file.read())
region_combined_text = "\n\n".join(region_texts)
region_sentences = split_sentences(region_combined_text)
region_sentence_embeddings = model.encode(region_sentences, convert_to_tensor=True)




'''find the matched description for tables 1 to 4 on page 1'''
# The target description
for tab_idx in range(1,5):
    file_path = f"./sheet/_page1_table{tab_idx}.csv"
    tab = extract_text_from_csv(file_path)
    tab_embedding = model.encode(tab, convert_to_tensor=True)

    # Find the match by considering cosine similarities between the target description and all sentences
    cosine_scores = util.pytorch_cos_sim(tab_embedding, sentence_embeddings)[0]
    sorted_indices = np.argsort(np.array(cosine_scores))[::-1]
    filtered_indices = [idx for idx in sorted_indices if cosine_scores[idx] > 0.55]
    top_indices = filtered_indices[:5]
    print(f"... table {tab_idx} ...:")
    print(" '' ", tab, " '' ")
    print('\n')
    for i, idx in enumerate(top_indices):
        print(f"Top {i+1} match with score {cosine_scores[idx]}:", sentences[idx])
    print('\n')




'''find the matched description for tables 5 to 7 on page 1'''
# prefix info for each table
prefix_dix = {5:'Revenue Growth quarter 3 2024',
              6:'Revenues by Business Segments',
              7:'Revenues by Client Geography'}

# find the match by considering cosine similarities between the target description and all sentences in each table
for tab_idx in [5,6,7]:
    print(f"... table {tab_idx} ...:")

    if tab_idx == 5: #general
        target_text_embeddings = sentence_embeddings
        target_text = sentences
    elif tab_idx == 6: #Business sector
        target_text_embeddings = sector_sentence_embeddings
        target_text = sector_sentences
    elif tab_idx == 7: #region sector
        target_text_embeddings = region_sentence_embeddings
        target_text = region_sentences
    
    file_path = f'./sheet/_page1_table{tab_idx}.csv'
    if tab_idx == 5:
        df = pd.read_csv(file_path)
        extracted_df = df[['Unnamed: 0', 'CC']]
    else:
        df = pd.read_csv(file_path,header=1)
        extracted_df = df[['Unnamed: 0', 'CC']]
        extracted_df.replace(r'\((.*?)\)', r'-\1', regex=True, inplace=True)
    
    for index, row in extracted_df.iterrows():
        first_column_value = row['Unnamed: 0']
        cc_value = row['CC'].replace('%', '')
        row_text = ': '.join([first_column_value, f'constant currency {cc_value}%'])
        for key, value in replacements.items():
            row_text = row_text.replace(key, value)
        
        row_text = ' '.join([prefix_dix[tab_idx],row_text])

        row_text_embedding = model.encode(row_text, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(row_text_embedding, target_text_embeddings)[0]
        sorted_indices = np.argsort(np.array(cosine_scores))[::-1]
        filtered_indices = [idx for idx in sorted_indices if cosine_scores[idx] > 0.3]
        top_indices = filtered_indices[:5]
        print(" '' ", row_text, " '' ")
        for i, idx in enumerate(top_indices):
            print(f"Top {i+1} match with score {cosine_scores[idx]}:", target_text[idx])
        print('\n')

    print('\n')
                



'''find the matched description for table 1 on page 2'''
file_path = f'./sheet/_page2_table1.csv'
df = pd.read_csv(file_path, header=1)
extracted_df = df[['Unnamed: 0', "Dec 31, 2023", "Sep 30, 2023", "Dec 31, 2022"]]
target_text_embeddings = sentence_embeddings
target_text = sentences

prefix_header = ''
for index, row in extracted_df.iterrows():

    header = row['Unnamed: 0']
    if header == 'Effort' or header == 'Utilization':
        prefix_header = header
        continue
    else:
        header = ' '.join([prefix_header,header])
        date_1 = f"Dec 31, 2023: {row['Dec 31, 2023']}%"
        date_2 = f"Sep 30, 2023: {row['Sep 30, 2023']}%"
        date_3 = f"Dec 31, 2022: {row['Dec 31, 2022']}%"
        row_text = f"{header}, {date_1}, {date_2}, {date_3}"

        row_text_embedding = model.encode(row_text, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(row_text_embedding, target_text_embeddings)[0]
        sorted_indices = np.argsort(np.array(cosine_scores))[::-1]
        filtered_indices = [idx for idx in sorted_indices if cosine_scores[idx] > 0.3]
        top_indices = filtered_indices[:5]
        print(" '' ", row_text, " '' ")
        for i, idx in enumerate(top_indices):
            print(f"Top {i+1} match with score {cosine_scores[idx]}:", target_text[idx])
        print('\n')

    print('\n')
    print('\n')




'''find the matched description for table 1 on page 3'''
file_path = f'./sheet/_page3_table1.csv'
extracted_df = pd.read_csv(file_path)
target_text_embeddings = sentence_embeddings
target_text = sentences

for index, row in extracted_df.iterrows():

    header = row['Particulars']
    if header == "Operating Expenses":
        continue
    date_1 = f"Dec 31, 2023: {row['Dec 31, 2023']}"
    date_2 = f"Sep 30, 2023: {row['Dec 31, 2022']}"
    date_3 = f"Growth in doller: {row['Growth %']}"
    row_text = f"{header}, {date_1}, {date_2}, {date_3}"
    for key, value in replacements.items():
        row_text = row_text.replace(key, value)
    
    row_text_embedding = model.encode(row_text, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(row_text_embedding, target_text_embeddings)[0]
    sorted_indices = np.argsort(np.array(cosine_scores))[::-1]
    filtered_indices = [idx for idx in sorted_indices if cosine_scores[idx] > 0.3]
    top_indices = filtered_indices[:5]
    print(" '' ", row_text, " '' ")
    for i, idx in enumerate(top_indices):
        print(f"Top {i+1} match with score {cosine_scores[idx]}:", target_text[idx])
    print('\n')

    print('\n')
