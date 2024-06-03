# symmary_sentiment (Text Preprocessing only and Sentiment Analysis will follow)

## Introduction

This project focuses on preprocessing a text file, typically obtained from transcripts of earnings calls, for further analysis. The preprocessing steps clean and structure the text to make it suitable for downstream tasks such as sentiment analysis.

## Preprocessing Steps

### 1. Read the File

The text file is read into a raw string using Python's built-in `open` function with UTF-8 encoding.

### 2. Remove Unwanted Lines

Lines starting with specific unwanted phrases are removed. These include:
- `FINAL TRANSCRIPT`
- `Tata Consultancy Services Ltd (TCS IN Equity)`
- `2024-01-11`
- `Page X of 24` (where `X` is a number from 1 to 24)

This is achieved using regular expressions to match and delete these lines.

### 3. Normalize Whitespace

Multiple spaces and newline characters are normalized:
- Multiple spaces are reduced to a single space.
- Multiple newline characters separating sentences are removed.

### 4. Combine Sentences Within Paragraphs

Sentences within paragraphs are combined correctly. This involves:
- Splitting the text into paragraphs using double newlines (`\n\n`).
- Combining lines within each paragraph, ensuring that sentences are concatenated correctly based on punctuation.

### Code

The code to achieve these preprocessing steps is as follows:

```python
import re

def read_file_to_raw_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_string = file.read()
    
    def combine_sentences_within_paragraphs(text):
        # Remove lines starting with unwanted phrases
        text = re.sub(r'^\s*FINAL TRANSCRIPT.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*Tata Consultancy Services Ltd \(TCS IN Equity\).*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*2024-01-11.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*Page \d+ of 24.*$', '', text, flags=re.MULTILINE)
        
        # Remove multiple spaces and newlines
        text = re.sub(r'\s*\n\s*', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        
        # Combine lines within paragraphs
        paragraphs = text.split('\n\n') 
        combined_paragraphs = []
        for paragraph in paragraphs:
            lines = paragraph.split('\n') 
            combined_lines = []
            for line in lines:
                if combined_lines and not re.match(r'[.!?]$', combined_lines[-1].strip()):
                    combined_lines[-1] += ' ' + line.strip()
                else:
                    combined_lines.append(line.strip())
            combined_paragraphs.append(' '.join(combined_lines))
        return '\n\n'.join(combined_paragraphs)

    cleaned_string = combine_sentences_within_paragraphs(raw_string)

    return cleaned_string 

# Example usage
file_path = 'path_to_your_file.txt'
cleaned_text = read_file_to_raw_string(file_path)

with open('cleaned_file.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_text)
