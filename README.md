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
- #sentences in summary: 7
- positive: 3 / 7
- negative: 4 / 7
- neutral: 0 / 7

-- Q&A 
- #sentences in summary: 94
- positive: 51 / 94
- negative: 43 / 94
- neutral: 0 / 94


### 2. Tata: 

-- presentation 
- #sentences in summary: 38
- positive: 28 / 38
- negative: 10 / 38
- neutral: 0 / 38

-- Q&A 
- #sentences in summary: 51
- positive: 29 / 51
- negative: 22 / 51
- neutral: 0 / 51


### 3. Wipro: 

-- presentation 
- #sentences in summary: 24
- positive: 14 / 24
- negative: 10 / 24
- neutral: 0 / 24

-- Q&A 
- #sentences in summary: 28
- positive: 18 / 28
- negative: 10 / 28
- neutral: 0 / 28

## Sector/Industry Performance Comparisions

### 1. Infosys: 
- technology: Mention count 7. Sector-wise sentiment 0.7057794077055795.
- energy: Mention count 4. Sector-wise sentiment 0.5113033056259155.
- healthcare: Mention count 1. Sector-wise sentiment 0.9998045563697815.
- manufacturing: Mention count 3. Sector-wise sentiment 0.9501329064369202.
- marketing: Mention count 1. Sector-wise sentiment 0.9678220152854919.
- finance: Mention count 1. Sector-wise sentiment 0.7860661745071411.
- retail: Mention count 4. Sector-wise sentiment 0.9579408317804337.
- communication: Mention count 1. Sector-wise sentiment 0.8508766293525696.

### 2. Tata: 
- technology: Mention count 28. Sector-wise sentiment 0.8984409634556089.
- marketing: Mention count 6. Sector-wise sentiment 0.6597093443075815.
- retail: Mention count 4. Sector-wise sentiment 0.9619636684656143.
- energy: Mention count 1. Sector-wise sentiment 0.9991719722747803.
- healthcare: Mention count 2. Sector-wise sentiment 0.8714967966079712.
- finance: Mention count 2. Sector-wise sentiment 0.9895267486572266.
- communication: Mention count 2. Sector-wise sentiment 0.9969807267189026.

### 3. Wipro: 
- technology: Mention count 14. Sector-wise sentiment 0.5660176532609122.
- healthcare: Mention count 5. Sector-wise sentiment 0.26656781435012816.
- energy: Mention count 1. Sector-wise sentiment -0.9567864537239075.
- marketing: Mention count 3. Sector-wise sentiment 0.3463961084683736.
- manufacturing: Mention count 1. Sector-wise sentiment 0.9990382194519043.
- finance: Mention count 4. Sector-wise sentiment 0.4955984652042389.



## Guidance Comparisons

### 1. Infosys: 
- `Based on the performance in the first three quarters and our outlook for Q4, we are tightening our revenue growth guidance for financial year '24 to 1.5% to 2% in constant currency.` {'label': 'NEGATIVE', 'score': 0.9918830394744873}
- `Our operating margin guidance for financial year '24 remains unchanged at 20% to 22%.` {'label': 'NEUTRAL', 'score': 0.9753782749176025}
- `Driven by our YTD growth of 1.8% in CC terms and Q4 outlook, we have revised our revenue growth guidance for FY '24 from 1% to 2.5% previously to 1.5% to 2% in constant currency terms.` {'label': 'NEGATIVE', 'score': 0.9831820130348206}
- `We retain our margin guidance band for the year at 20% to 22%.` {'label': 'POSITIVE', 'score': 0.9815574884414673}

### 2. Tata:
- `As you are aware, we don't provide specific revenue or
earnings guidance.`

### 3. Wipro: 
- `One, our IT services revenue for the quarter is at the top end of the guidance.` {'label': 'NEGATIVE', 'score': 0.9027857780456543}
- `Onto our guidance now for the next quarter.` {'label': 'POSITIVE', 'score': 0.9612802267074585}
- `Following a quarter of strong execution, our revenue is at the top end of the guidance range.` {'label': 'POSITIVE', 'score': 0.9400153756141663}
- `Finally, I would like to summarize the guidance for Q4, This translates to a sequential guidance of minus 1.5% to a plus 0.5% in constant currency terms.` {'label': 'NEGATIVE', 'score': 0.9979019165039062}



## Region Comparisons

### 1. Infosys: 

- North America:
#mentions: 1.
Region-wise sentiment: 1.00.

- Europe:
#mentions: 2.
Region-wise sentiment: 1.00.

- Asia:
#mentions: 1.
Region-wise sentiment: 1.00.

### 2. Tata: 

- North America:
#mentions: 4.
Region-wise sentiment: 0.52.

- Europe:
#mentions: 5.
Region-wise sentiment: 0.98.

- Oceania:
#mentions: 1.
Region-wise sentiment: 1.00.

### 3. Wipro: 

- North America:
#mentions: 2.
Region-wise sentiment: 0.99.

- Europe:
#mentions: 3.
Region-wise sentiment: 0.33.
