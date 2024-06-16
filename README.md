# Assignment 1

## Introduction

This project focuses on processing transcripts of earnings calls for summary, sentiment analysis, and comparisons. We first introduce the preprocessing steps and then enumerate the analysis results.

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

After text pre-processing steps, we separately build clean presentation text and clean Q&A paris.

## Sentiment Comparisons
### We first build the summary texts separately for presentation and Q&A for each of the three companies (see `summaries` directory), and then analyse the summary.

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
### For each self-defined sector, we extract the relevant sentences from the raw text, count their occurrences, and calculate the average sentiment score for each sector based on the extracted sentences.

### 1. Infosys: 
- technology: #mentions 7. Sector-wise sentiment 0.7057794077055795.
- energy: #mentions 4. Sector-wise sentiment 0.5113033056259155.
- healthcare: #mentions 1. Sector-wise sentiment 0.9998045563697815.
- manufacturing: #mentions 3. Sector-wise sentiment 0.9501329064369202.
- marketing: #mentions 1. Sector-wise sentiment 0.9678220152854919.
- finance: #mentions 1. Sector-wise sentiment 0.7860661745071411.
- retail: #mentions 4. Sector-wise sentiment 0.9579408317804337.
- communication: #mentions 1. Sector-wise sentiment 0.8508766293525696.

### 2. Tata: 
- technology: #mentions 28. Sector-wise sentiment 0.8984409634556089.
- marketing: #mentions 6. Sector-wise sentiment 0.6597093443075815.
- retail: #mentions 4. Sector-wise sentiment 0.9619636684656143.
- energy: #mentions 1. Sector-wise sentiment 0.9991719722747803.
- healthcare: #mentions 2. Sector-wise sentiment 0.8714967966079712.
- finance: #mentions 2. Sector-wise sentiment 0.9895267486572266.
- communication: #mentions 2. Sector-wise sentiment 0.9969807267189026.

### 3. Wipro: 
- technology: #mentions 14. Sector-wise sentiment 0.5660176532609122.
- healthcare: #mentions 5. Sector-wise sentiment 0.26656781435012816.
- energy: #mentions 1. Sector-wise sentiment -0.9567864537239075.
- marketing: #mentions 3. Sector-wise sentiment 0.3463961084683736.
- manufacturing: #mentions 1. Sector-wise sentiment 0.9990382194519043.
- finance: #mentions 4. Sector-wise sentiment 0.4955984652042389.



## Guidance Comparisons
### We extract the relevant sentences regarding `guidance` information from the raw text, and calculate the sentiment score for extracted sentence.

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
### For each self-defined region, we extract the relevant sentences from the raw text, count their occurrences, and calculate the average sentiment score for each region based on the extracted sentences.

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


## Extracted tables for Infosys
- see `extracted_excel` as the tables in the usable form
- Fro 
