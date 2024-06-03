# Summary Sentiment Analysis

## Introduction

This project focuses on preprocessing a text file, typically obtained from transcripts of earnings calls, for further sentiment analysis. We first introduce the preprocessing steps here cleaning and structuring the text to make it suitable for downstream sentiment analysis tasks.

## Preprocessing Steps

### 1. Read the File

The text file is read into a raw string using Python's built-in `open` function with UTF-8 encoding.

### 2. Remove Unwanted Lines

Lines starting with specific unwanted phrases are removed. These include but not limited:
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
- removing unwanted 
