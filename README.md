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
### For each self-defined sector, we extract the relevant sentences from the raw text, count their occurrences, and calculate the average sentiment score for each sector based on the extracted sentences. Details on self-defined sector information can be found in `main.py`.

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


## Extracted tables for Infosys (Updated version on 21 Jul 2024)
### Overall workflow
- We employ `sheet.py` to extract and analyse tables
- Automatically extract tables from the PDF using `pdfplumber` pakcage 
- Use custom dictionaries to clarify the information in the extracted tables (e.g., convert YOY to year-on-year, CC to constant currency, ($) to (in doller term) etc.) 
- Extract the information from the tables and embed it using `'all-MiniLM-L6-v2'` model imported from `SentenceTransformer` pakcage
- Also embed the information from the cleaned earning call text, the extracted sub-texts from Sector/Industry Performance Comparisions and Region Comparisons (tasks above)  
- Calculate cosine scores between the two embeddings to identify connections between the descriptions in the earnings call and the information presented in the tables.
- From the examples below, we can clearly find that most info in the extracted tables is described in the earning call, but some negative info is only vagauly metnioned in the earning call, can by connecting them, we provide quite vital insights.
- The examples below demonstrate that most information in the extracted tables is discussed in the earnings call. However, some negative details (in the table) are only vaguely mentioned (in the earnings call). By connecting these pieces of information, we provide crucial insights.
  
### Result example 1: first table on page 1
- The first extracted table on page 1 is saved as `_page1_table1.csv` in the `sheet` folder 
- The infomation in this table includes data like `Third Quarter: -1.0% YoY & QoQ CC growt`
- The top 3 matching descriptions in the earnings call are:
  - Top 1 match with score 0.7658648490905762: Our Q3 revenue declined by 1% quarter-on-quarter and 1% year-on-year in constant currency terms
  - Top 2 match with score 0.6902984380722046: Sequentially, revenues similarly declined by 1% in constant currency and 1.2% in dollar terms
  - Top 3 match with score 0.6568119525909424: Coming to our Q3 results, revenues declined by 1% year-on-year in constant currency
- The result (top 1) is the corresponding description that closely aligns with the information in the table showing `Q3 revenue declined by 1% quarter-on-quarter and 1% year-on-year`

### Result example 2: second table on page 1
- The second extracted table on page 1 is saved as `_page1_table2.csv` in the `sheet` folder 
- The infomation in this table includes data like `Third Quarter: 20.5% Operating margin`
- The top 3 matching descriptions in the earnings call are:
  - Top 1 match with score 0.8842840194702148: Our operating margin was at 20.5%
  - Top 2 match with score 0.6875313520431519: Our operating margin guidance for financial year '24 remains unchanged at 20% to 22%
  - Top 3 match with score 0.6250747442245483: Operating margins for Q2 were 20.5%, a decline of 70 basis points sequentially, bringing the ninemonth margins to 20.8%, which is within the guidance banked for the year
- The result (top 1) is the corresponding description that closely aligns with the information in the table showing `operating margin was at 20.5% in the third quarter`

### Result example 3: fourth table on page 1
- The fourth extracted table on page 1 is saved as `_page1_table4.csv` in the `sheet` folder 
- The infomation in this table includes data like `Third Quarter: $3.2 bn Large deal TCV (71% net new)`
- The top 3 matching descriptions in the earnings call are:
  - Top 1 match with score 0.7026665210723877: Large deal momentum continued and deal TCV of Q3 was $3.2 billion with 71% net new
  - Top 2 match with score 0.6287296414375305: Consequently, our large deal TCV is over $13 billion, which is the highest ever for any comparative period
  - Top 3 match with score 0.603040337562561: Large deals were at $3.2 billion, 71% of this was net new
- The results (top 1 and top 3) are the corresponding descriptions that closely align with the information in the table showing `Large deal TCV of Q3 was $3.2 billion with 71% net new`

### Result example 4: fifth table on page 1
- The fifth extracted table on page 1 is saved as `_page1_table5.csv` in the `sheet` folder 
- The infomation in this table includes data like `Revenue Growth- Q3 24; QoQ growth (%) Reported -1.2 CC -1.0; YoY growth (%) Reported 0.1 CC -1.0%`
- For first row `QoQ growth`, the top 4 matching descriptions in the earnings call are:
  - Top 1 match with score 0.694708526134491: Coming to our Q3 results, revenues declined by 1% year-on-year in constant currency
  - Top 2 match with score 0.6926833391189575: Our Q3 revenue declined by 1% quarter-on-quarter and 1% year-on-year in constant currency terms
  - Top 3 match with score 0.6819989085197449: Revenue for nine months increased by 1.8% in constant currency and 2.5% in USD terms
  - Top 4 match with score 0.680861234664917: Sequentially, revenues similarly declined by 1% in constant currency and 1.2% in dollar terms
- The results (top 2 and top 4) are the corresponding descriptions closely align with the information in the table showing `Revenue Growth on Q3 2024 is with QoQ growth as Reported -1.2% and CC -1.0%`
- For second row `YoY growth`, the top 4 matching descriptions in the earnings call are:
  - Top 1 match with score 0.716171383857727: Coming to our Q3 results, revenues declined by 1% year-on-year in constant currency
  - Top 2 match with score 0.7095981240272522: Revenue for nine months increased by 1.8% in constant currency and 2.5% in USD terms
  - Top 3 match with score 0.6835198402404785: Sequentially, revenues similarly declined by 1% in constant currency and 1.2% in dollar terms
  - Top 4 match with score 0.6736979484558105: Our Q3 revenue declined by 1% quarter-on-quarter and 1% year-on-year in constant currency terms
- The results (top 1 and top 4) are the corresponding descriptions that closely align with the information in the table showing `Revenue Growth on Q3 2024 is with YoY growth as Reported 0.1% and CC -1.0%`

### Result example 5: sixth table on page 1
- The sixth extracted table on page 1 is saved as `_page1_table6.csv` in the `sheet` folder 
- The infomation in this table includes data about `Revenues by Business Segments`
- For the third row `Communication; YoY growth Reported (7.3); CC (8.0)`, the top 2 matching descriptions in the earnings call are:
  - Top 1 match with score 0.4655866026878357: We signed eight deals in manufacturing, six in FS, four in EURS, two each in retail and communication and one in others
  - Top 2 match with score 0.3642865717411041: In the retail segment, cost takeouts and consolidation remain the primary focus for the clients
- The result (top 1) is the corresponding descriptions that align with the information in the table indicating `communication is with YoY growth Reported -7.3% and CC -8.0%`. While the table clearly shows a decline in the communication segment, the earnings call only vaguely references two deals each in retail and communication without explicitly disclosing the decline. This suggests that the company might be downplaying negative performance in the earnings call. Therefore, extracting and comparing table data with the earnings call text, as we have done, is crucial for uncovering such discrepancies.
- For the fifth row `Manufacturing; YoY growth Reported 12.5; CC 10.6`, the top 2 matching descriptions in the earnings call are:
  - Top 1 match with score 0.48526206612586975: Manufacturing segment continues to deliver strong performance on the back of new deal wins and ramp up of earlier large deals signed
  - Top 2 match with score 0.37917593121528625: We signed eight deals in manufacturing, six in FS, four in EURS, two each in retail and communication and one in others
- The result (top 1) is the corresponding descriptions that closely align with the information in the table showing that `Manufacturing is with strong performance with YoY growth Reported 12.5% and CC 10.6%`

### Additionally, I have presented the results for the tables `Revenues by Client Geography`, `Effort & Utilization – Consolidated IT Services`, and `Consolidated Statement of Comprehensive Income for Nine Months Ended (Extracted from IFRS Financial Statement)`. These are all saved in the `sheet` folder, and their corresponding details are readily accessible.
