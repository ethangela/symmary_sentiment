import fitz
import openai
from transformers import pipeline
import os
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from collections import defaultdict, Counter

# Load the pipelines
# summarizer = pipeline("summarization")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analysis = pipeline('sentiment-analysis')

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def summarize_text(text):
    summary = summarizer(text, max_length=250, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def summarize_qa_pair(q, a): #TODO
    
    text_length = len(q.split())
    max_length = int(text_length * 1)
    min_length = int(text_length * 0.1)
    summary = summarizer(q, max_length=max_length, min_length=min_length, do_sample=False)
    q = summary[0]['summary_text']

    text_length = len(a.split())
    max_length = int(text_length * 1)
    min_length = int(text_length * 0.1)
    summary = summarizer(a, max_length=max_length, min_length=min_length, do_sample=False)
    a = summary[0]['summary_text']
    
    # return f"{q} {a}" #TODO
    return f"{a}"
    
def analyze_sentiment(text):
    sentences = sent_tokenize(text)
    print('len of sentences: ', len(sentences))
    sentiments = []
    for sentence in sentences:
        if sentence.strip():  # Check if the sentence is not empty
            sentiments.extend(sentiment_analysis(sentence))
    return sentiments

def summarize_sentiment(sentiment_results):
    positive = sum([1 for result in sentiment_results if result['label'] == 'POSITIVE'])
    negative = sum([1 for result in sentiment_results if result['label'] == 'NEGATIVE'])
    neutral = sum([1 for result in sentiment_results if result['label'] == 'NEUTRAL'])
    total = len(sentiment_results)
    print(f'positive: {positive} / {total}')
    print(f'negative: {negative} / {total}')
    print(f'neutral: {neutral} / {total}')

def extract_sentences_by_sector(text, sectors_keywords):
    sentences = re.split(r'(?<=[.!?]) +', text)
    sector_sentences = defaultdict(list)
    for sentence in sentences:
        matched_sectors = []
        for sector, keywords in sectors_keywords.items():
            if re.search(r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b', sentence, re.IGNORECASE):
                matched_sectors.append(sector)
        for sector in matched_sectors:
            sector_sentences[sector].append(sentence)
    return sector_sentences

def analyze_exposure(sector_sentences):
    exposure = {sector: len(sentences) for sector, sentences in sector_sentences.items()}
    return exposure

def evaluate_exposure_strength(keyword_counts, total_sentences):
    exposure_strength = {}
    for keyword, count in keyword_counts.items():
        exposure_strength[keyword] = count / total_sentences
    
    return exposure_strength

def aggregate_sentiment_scores(sector_sentences):
    sector_sentiments = {sector: [] for sector in sector_sentences}
    
    for sector, sentences in sector_sentences.items():
        for sentence in sentences:
            sentiment = sentiment_analysis(sentence)[0]
            sector_sentiments[sector].append(sentiment)
    
    # Calculate average sentiment score for each sector
    sector_avg_sentiment = {}
    for sector, sentiments in sector_sentiments.items():
        if sentiments:
            avg_score = sum(s['score'] if s['label'] == 'POSITIVE' else -s['score'] for s in sentiments) / len(sentiments)
            sector_avg_sentiment[sector] = avg_score
        else:
            sector_avg_sentiment[sector] = None
    
    return sector_avg_sentiment

def extract_guidance_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    guidance_sentences = [sentence for sentence in sentences if 'guidance' in sentence.lower()]
    return guidance_sentences

def extract_sentences_by_region(text, regions):
    sentences = re.split(r'(?<=[.!?]) +', text)
    region_sentences = defaultdict(list)
    for sentence in sentences:
        for region, keywords in regions.items():
            if any(keyword in sentence.lower() for keyword in keywords):
                region_sentences[region].append(sentence)
    return region_sentences

def analyze_region_performance(region_sentences, sentiment_analysis):
    region_performance = {}
    for region, sentences in region_sentences.items():
        sentiments = sentiment_analysis(sentences)
        scores = [sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score'] for sentiment in sentiments]
        region_performance[region] = {
            'average_sentiment': sum(scores) / len(scores) if scores else 0,
            'number_of_mentions': len(scores)
        }
    return region_performance



def summary_pipelines(file_path_prior, qa_pair=1, base=1):
    
    #presentation
    pt_path = file_path_prior + '_pres.txt'
    pt_summary = []
    for pt in read_text_file(pt_path).split('\n\n'):
        pt_summary.append(summarize_text(pt))
    pt_summary = '\n'.join(pt_summary) #pre summary 
    pt_path = file_path_prior + '_pres_sum.txt'
    with open(pt_path, 'w', encoding='utf-8') as file:
        file.write(pt_summary)

    #q&a pairs
    def extract_qa_pairs(text):
        lines = text.split('\n')
        
        qa_pairs = []
        current_q = None
        current_a = None
        
        for line in lines:
            if line.startswith('Q:'):
                if current_q and current_a:  # If there's an existing Q&A pair, save it
                    qa_pairs.append((current_q, current_a))
                    current_a = None  # Reset the answer
                current_q = line[3:]#'Question: ' + line[3:]  # Start a new question
            elif line.startswith('A:'):
                if current_a:  # If there's an existing answer, add to it
                    current_a += " " + line[3:]#'Answer: ' + line[3:]
                else:
                    current_a = line[3:]#'Answer: ' + line[3:]  # Start a new answer
            else:
                if current_a:  # Continue the current answer if line doesn't start with Q or A
                    current_a += " " + line

        # Append the last Q&A pair if exists
        if current_q and current_a:
            qa_pairs.append((current_q, current_a))
        
        return qa_pairs

    qa_summary = []
    for idx in range(base,base+qa_pair):
        try:
            qa_path = file_path_prior + f'_qa_{idx}.txt'
            qa_pairs = extract_qa_pairs(read_text_file(qa_path))

            summaries = []
            for q, a in qa_pairs:
                summary = summarize_qa_pair(q, a)
                summaries.append(summary)
            combined_summary = ". ".join(summaries)
            qa_summary.append(combined_summary)
        except:
            continue
    qa_summary = '\n'.join(qa_summary)
    pt_path = file_path_prior + '_qa_sum.txt'
    with open(pt_path, 'w', encoding='utf-8') as file:
        file.write(qa_summary)
    
def sentiment_pipelines(file_path_prior): #TODO print to the file
    #presentation
    pt_path = file_path_prior + '_pres_sum.txt'
    sent_list = analyze_sentiment(read_text_file(pt_path))
    summarize_sentiment(sent_list)

    #qa
    pt_path = file_path_prior + '_qa_sum.txt'
    sent_list = analyze_sentiment(read_text_file(pt_path))
    summarize_sentiment(sent_list)

def sector_pipelines(file_path_prior): #TODO print to the file
    sector_words = {
        'energy': ['energy', 'energy utilities', 'energies', 'oil', 'gas', 'renewable'],
        'finance': ['finance', 'banking', 'insurance', 'capital', 'bank'],
        'healthcare': ['healthcare', 'medical', 'pharmaceutical', 'biotech', 'life sciences'],
        'technology': ['technology', 'generative AI', 'tech', 'software development', 'hardware', 'IT', 'digital', 'cloud', 'high-tech'],
        'retail': ['consumer goods', 'retail', 'apparel', 'food', 'beverages'],
        'manufacturing': ['manufacturing'],
        'marketing': ['client analytics', 'sales', 'marketing', 'knowledge analysis', 'personalization'],
        'communication':['communication']
    }

    pt_path = file_path_prior + '_pres.txt'
    sector_sentences = extract_sentences_by_sector(read_text_file(pt_path), sector_words)
    exposure = analyze_exposure(sector_sentences)
    sector_avg_sentiment = aggregate_sentiment_scores(sector_sentences)
    for sector, sentences in sector_sentences.items():
        print(f"- {sector}: Mention count {len(sentences)}. Sector-wise sentiment {sector_avg_sentiment[sector]}.")
        # for i, sentence in enumerate(sentences, start=1):
        #     print(f"  {i}. {sentence}")

def guidance_pipelines(file_path_prior): #TODO print to the file
    pt_path = file_path_prior + '_pres.txt'
    guidance_sentences = extract_guidance_sentences(read_text_file(pt_path))
    for i, gd in enumerate(guidance_sentences):
        print(i, gd, sentiment_analysis(gd)[0])

def region_pipelines(file_path_prior): #TODO print to the file
    pt_path = file_path_prior + '_pres.txt'
    regions = {
        'North America': ['america', 'north america', 'usa', 'united states', 'canada'],
        'Europe': ['europe', 'uk', 'united kingdom', 'germany', 'france', 'italy', 'spain'],
        'Asia': ['asia', 'china', 'india', 'japan', 'south korea', 'indonesia'],
        'South America': ['latin america', 'south america', 'brazil', 'argentina', 'chile'],
        'Africa': ['africa', 'south africa', 'nigeria', 'egypt'],
        'Oceania': ['oceania', 'australia', 'new zealand']
    }
    region_sentences = extract_sentences_by_region(read_text_file(pt_path), regions)
    region_performance = analyze_region_performance(region_sentences, sentiment_analysis)
    # print("Region-wise Performance Analysis:")
    for region, performance in region_performance.items():
        print(f"- {region}:")
        print(f"#mentions: {performance['number_of_mentions']}.")
        print(f"Region-wise sentiment: {performance['average_sentiment']:.2f}.")



# def region_pipelines():
#     'Region-wise, we signed 10 large deals in America, nine in Europe and three in ROW, and one in India.'

if __name__ == "__main__":
    

    #summary
    file_path_prior = './assignment1/infos/Infosys_clean'
    summary_pipelines(file_path_prior, qa_pair=14, base=1)
    file_path_prior = './assignment1/tata/Tata_clean'
    summary_pipelines(file_path_prior, qa_pair=14, base=1)
    file_path_prior = './assignment1/wipro/Wipro_clean'
    summary_pipelines(file_path_prior, qa_pair=6, base=1)


    #sentiment
    print('......Sentiment comparison......')
    print('Infosys: ')
    file_path_prior = './assignment1/infos/Infosys_clean'
    sentiment_pipelines(file_path_prior)

    print('Tata: ')
    file_path_prior = './assignment1/tata/Tata_clean'
    sentiment_pipelines(file_path_prior)

    print('Wipro: ')
    file_path_prior = './assignment1/wipro/Wipro_clean'
    sentiment_pipelines(file_path_prior)


    #Sector and industry exposure/performance
    print('Infosys: ')
    file_path_prior = './assignment1/infos/Infosys_clean'
    sector_pipelines(file_path_prior)

    print('Tata: ')
    file_path_prior = './assignment1/tata/Tata_clean'
    sector_pipelines(file_path_prior)

    print('Wipro: ')
    file_path_prior = './assignment1/wipro/Wipro_clean'
    sector_pipelines(file_path_prior)


    #guidance performance
    print('Infosys: ')
    file_path_prior = './assignment1/infos/Infosys_clean'
    guidance_pipelines(file_path_prior)

    print('Tata: ')
    file_path_prior = './assignment1/tata/Tata_clean'
    guidance_pipelines(file_path_prior)

    print('Wipro: ')
    file_path_prior = './assignment1/wipro/Wipro_clean'
    guidance_pipelines(file_path_prior)


    #region wise performance
    print('Infosys: ')
    file_path_prior = './assignment1/infos/Infosys_clean'
    region_pipelines(file_path_prior)

    print('Tata: ')
    file_path_prior = './assignment1/tata/Tata_clean'
    region_pipelines(file_path_prior)

    print('Wipro: ')
    file_path_prior = './assignment1/wipro/Wipro_clean'
    region_pipelines(file_path_prior)
