# Summary Sentiment Analysis

## Introduction

This project focuses on processing transcripts of earnings calls for summary, sentiment analysis, and comparisons. We first introduce the preprocessing steps here cleaning and structuring the text to make it suitable for downstream tasks.

## Preprocessing Steps

### 1. Remove Unwanted Items

Lines starting with or containing specific unwanted phrases are removed. These include but not limited:
- `FINAL TRANSCRIPT`
- `Tata Consultancy Services Ltd (TCS IN Equity)`
- `2024-01-11`
- `Page X of 24` (where `X` is a number from 1 to 24)
- `{BIO X <GO>}` (where `X` is a random number)
- Names of all particcipants
- Irrelevant phrases like `thank you`, `happy new year`, `over to you` etc. 

### 2. Normalize Whitespace

Multiple spaces and newline characters are normalized:
- Multiple spaces are reduced to a single space.
- Multiple newline characters separating sentences are removed.

### 3. Separate to Presentation and Q&A texts

After text pre-processing steps, we need clean presentation text as well as the list of clean Q&A paris. The obtained results can found in this directory.

### 4. Downstream Summary, Sentiment Analysis, and Comparisons (To-Be-Continued).

