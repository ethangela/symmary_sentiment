import re

def read_file_to_raw_string(file_path, name):
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_string = file.read()
    
    def combine_sentences_within_paragraphs(text):
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
    
    def remove_specific_lines(text):
        # pattern = r'^(FINAL TRANSCRIPT|Tata Consultancy Services Ltd \(TCS IN Equity\)|2024-01-11|Page \d{1,2} of 24).*'
        pattern = r'^\s*(FINAL TRANSCRIPT|Tata Consultancy Services Ltd \(TCS IN Equity\)|2024-01-11|Page \d{1,2} of 24).*'
        cleaned_text = '\n'.join(line for line in text.split('\n') if not re.match(pattern, line))
        return cleaned_text
    
    raw_string = remove_specific_lines(raw_string)
    raw_string = combine_sentences_within_paragraphs(raw_string)
    # cleaned_string = '\n'.join(cleaned_string.split('\n\n')) 
    return raw_string

def clean_data_info(data): #for info company
    """
    Returns:
        list, list: Returns two lists, one for the presentation which contains
        a sub list for each paragraph containing all its tokens and one for
        the Q&A which contains a sub list for each answer containing all its tokens.
    """
    

    '''remove disclarmier'''
    data = data.split("This transcript may not be 100 percent accurate", 1)[0]


    '''unwanted items'''
    undesired_lines = [
        "Thomson Reuters", "Refinitiv", "E D I T E D",
        "Q1", "Q2", "Q3", "Q4", 
        "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", 
        "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER",
        "*", "=", "-",
        "Corporate Participants", "Conference Call Participiants", "Other Participants", "Company Participants",
        "Operator"
        ]


    '''names in participants'''
    participants, data = data.split("Presentation", 1)
    participants = participants.split('\n\n')
    participants = '\n'.join(participants)
    participants = participants.split('\n')
    participants = [sentence for sentence in participants if not any(word in sentence for word in undesired_lines)]
    names = []
    for participant in participants:
        name = participant.split(',')[0]
        if name != '':
            names.append(name)
            first, last = name.split(' ')
            names.append(first)
            names.append(last)


    '''paragraph cleaning'''
    paragraphs = data.split('\n\n')  # Split text into paragraphs
    combined_paragraphs = []
    for paragraph in paragraphs:
        lines = paragraph.split('\n')  # Split paragraph into lines
        combined_lines = []
        for line in lines:
            if combined_lines and not re.match(r'[.!?]$', combined_lines[-1].strip()):
                combined_lines[-1] += ' ' + line.strip()
            else:
                combined_lines.append(line.strip())
        # if not ' '.join(combined_lines).strip().startswith('Operator'):
        combined_paragraphs.append(' '.join(combined_lines).strip())
    data = '\n\n'.join(combined_paragraphs)


    ''' get rid of unwanted things '''
    pattern = r'Q - \b[A-Z][a-zA-Z]+\s[A-Z][a-zA-Z]+ \{BIO \d+ <GO>\}'
    data = re.sub(pattern, 'Q:', data)
    pattern = r'A - \b[A-Z][a-zA-Z]+\s[A-Z][a-zA-Z]+ \{BIO \d+ <GO>\}'
    data = re.sub(pattern, 'A:', data)


    '''QA separate'''
    pres, qa = data.split("Questions And Answers", 1)


    '''pre cleaning'''
    def contains_non_relevant_word(sentence, non_relevant_words):
        for word in non_relevant_words:
            if word.lower() in sentence.lower():
                return True
        return False
    non_relevant_words = ['hi', 'hello', '{BIO', 'Happy New Year', 'pass on', 'good morning', 'good afternoon', 'good evening', 'good day', 'thank you', 
                          'all the best', 'hand it over', 'hand over', 'open up the call for questions', 'Thanks', 'Thank you', 'Okay.', 'Yeah.', 'thanks']

    dirty_lines = pres.split('\n\n')
    clean_lines = []
    for line in dirty_lines:
        if not line.startswith('Operator'):
            #remove name, hello, happy new year, good day, pass on etc. 
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', line)
            filtered_sentences = [sentence for sentence in sentences if not contains_non_relevant_word(sentence, non_relevant_words)]
            filtered_text = ' '.join(filtered_sentences)
            clean_lines.append(filtered_text)
    clean_pres = '\n\n'.join(clean_lines)
    
    with open('./assignment1/Infosys_clean_pres.txt', 'w') as file:
        file.write(clean_pres)


    '''QA cleaning'''
    pattern = r'(?=Operator Thank you[^.]*?\.)'
    qa_pairs = re.split(pattern, qa, flags=re.DOTALL)
    clean_qa_pairs = []

    for j,pair in enumerate(qa_pairs):
        if not pair.strip():
            continue
        pair = re.sub(r'^Operator.*$', '', pair, flags=re.MULTILINE).strip() # Remove the "Operator" sentence
        segment_list = pair.strip('\n').split('\n\n')
        clean_segment_list = []
        for i,sub_segment in enumerate(segment_list):
            '''further QA cleaning for each sub_sentence (to remove unwanted words)'''
            if sub_segment != '':
                segment_len = len(sub_segment.split(' '))
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sub_segment)
                # print(i, sentences)
                clean_segment_list.append(sub_segment)
        pair = '\n'.join(clean_segment_list)
        with open(f'./assignment1/Infosys_clean_qa_{j}.txt', 'w') as file:
            file.write(pair)






'''TATA'''
# file_path = '/Users/ethangela/Downloads/Jobs/mlp/assignment1/Tata Consultancy Services Ltd Earnings Call 2024111.txt'
# txt = read_file_to_raw_string(file_path)
# with open('./assignment1/Tata_output.txt', 'w') as file:
#         file.write(txt)

def clean_data(data, name): #for info company
    '''remove disclarmier'''
    data = data.split("This transcript may not be 100 percent accurate", 1)[0]


    '''unwanted items'''
    undesired_lines = [
        "Thomson Reuters", "Refinitiv", "E D I T E D",
        "Q1", "Q2", "Q3", "Q4", 
        "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", 
        "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER",
        "*", "=", "-",
        "Corporate Participants", "Conference Call Participiants", "Other Participants", "Company Participants",
        "Operator"
        ]


    '''names in participants'''
    # participants, data = data.split("Presentation", 1)
    # participants = participants.split('\n\n')
    # participants = '\n'.join(participants)
    # participants = participants.split('\n')
    # participants = [sentence for sentence in participants if not any(word in sentence for word in undesired_lines)]
    # names = []
    # for participant in participants:
    #     name = participant.split(',')[0]
    #     if name != '':
    #         names.append(name)
    #         first, last = name.split(' ')
    #         names.append(first)
    #         names.append(last)

    '''QA separate'''
    pres, qa = data.split("Questions And Answers", 1)
    
    with open(f'./assignment1/{name}_clean_pres.txt', 'w') as file:
        file.write(pres)


    '''QA cleaning'''
    pattern = r'(?=Operator Thank you[^.]*?\.)'
    qa_pairs = re.split(pattern, qa, flags=re.DOTALL)
    clean_qa_pairs = []

    for j,pair in enumerate(qa_pairs):
        if not pair.strip():
            continue
        pair = re.sub(r'^Operator.*$', '', pair, flags=re.MULTILINE).strip() # Remove the "Operator" sentence
        segment_list = pair.strip('\n').split('\n\n')
        clean_segment_list = []
        for i,sub_segment in enumerate(segment_list):
            '''further QA cleaning for each sub_sentence (to remove unwanted words)'''
            if sub_segment != '':
                segment_len = len(sub_segment.split(' '))
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sub_segment)
                # print(i, sentences)
                clean_segment_list.append(sub_segment)
        pair = '\n'.join(clean_segment_list)
        with open(f'./assignment1/{name}_clean_qa_{j}.txt', 'w') as file:
            file.write(pair)


# with open('./assignment1/Tata_output.txt', 'r') as file:
#     strings = file.read()
#     clean_data(strings)


'''Wipro'''
# file_path = '/Users/ethangela/Downloads/Jobs/mlp/assignment1/Wipro Ltd Earnings Call 2024112.txt'
# txt = read_file_to_raw_string(file_path)
# with open('./assignment1/Wipro_output.txt', 'w') as file:
#     file.write(txt)
with open('./assignment1/Wipro_output.txt', 'r') as file:
    strings = file.read()
    clean_data(strings,'Wipro')