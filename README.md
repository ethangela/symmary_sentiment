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

## Sentiment Comparisons

### 1. Infosys:
  
-- presentation 
len of sentences:  7
- positive: 3 / 7
- negative: 4 / 7
- neutral: 0 / 7

-- Q&A 
len of sentences:  94
positive: 51 / 94
negative: 43 / 94
neutral: 0 / 94


### 2. Tata: 

-- presentation 
- len of sentences:  38
- positive: 28 / 38
- negative: 10 / 38
- neutral: 0 / 38

-- Q&A 
- len of sentences:  51
- positive: 29 / 51
- negative: 22 / 51
- neutral: 0 / 51


### 3. Wipro: 

-- presentation 
- len of sentences:  24
- positive: 14 / 24
- negative: 10 / 24
- neutral: 0 / 24

-- Q&A 
- len of sentences:  28
- positive: 18 / 28
- negative: 10 / 28
- neutral: 0 / 28

