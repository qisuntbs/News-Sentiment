from os import path
import pandas as pd


def merged_lex():
    lm_xls = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')
    lm_p_df = pd.read_excel(lm_xls, 'Positive',
                            header=None, names=['p_senti'])
    lm_n_df = pd.read_excel(lm_xls, 'Negative',
                            header=None, names=['n_senti'])
    lm_p = list(lm_p_df['p_senti'])
    lm_n = list(lm_n_df['n_senti'])

    hl_p_file = open("./hl_2004/positive-words.txt", "r")
    hl_p_inter = hl_p_file.readlines()[30:]
    hl_p_file.close()
    hl_p = [w.replace('\n', '').upper() for w in hl_p_inter]

    hl_n_file = open("./hl_2004/negative-words.txt", "r")
    hl_n_inter = hl_n_file.readlines()[31:]
    hl_n_file.close()
    hl_n = [w.replace('\n', '').upper() for w in hl_n_inter]

    # take care of the inter-sections:
    for i in range(len(hl_p)):
        if hl_p[i] in lm_n:
            hl_p[i] = '__INTERLISTED__'
        elif hl_p[i] in hl_n:  # ENVIOUS, ENVIOUSLY, ENVIOUSNESS
            hl_p[i] = '__INTERLISTED__'
    for j in range(len(hl_n)):
        if hl_n[j] in lm_p:
            hl_n[j] = '__INTERLISTED__'
    for k in range(len(lm_p)):
        # Get rid of DESPITE in LM (positive) as it's a negate
        if lm_p[k] == 'DESPITE':
            lm_p[k] = '__INTERLISTED__'

    p_senti = lm_p + hl_p
    n_senti = lm_n + hl_n

    with open('./merged_lex/positive.txt', mode='w') as file:
        file.writelines(["%s\n" % item for item in p_senti])
    with open('./merged_lex/negative.txt', mode='w') as file:
        file.writelines(["%s\n" % item for item in n_senti])


class lexi:
    def __init__(self):
        if (not path.exists("./merged_lex/negative.txt")) |\
           (not path.exists("./merged_lex/positive.txt")):
            print('Loading the LM and HL lexicons...')
            merged_lex()
        p_file = open("./merged_lex/positive.txt", "r")
        p_senti_list = p_file.readlines()
        p_file.close()
        p_senti = [w.replace('\n', '') for w in p_senti_list]
        n_file = open("./merged_lex/negative.txt", "r")
        n_senti_list = n_file.readlines()
        n_file.close()
        n_senti = [w.replace('\n', '') for w in n_senti_list]

        # additions, exceptions, etc.
        n_senti.append('DEATHS')

        self.positive = p_senti
        self.negative = n_senti
        # VADER Model - Hutto and Gilbert (2014)
        # https://github.com/cjhutto/vaderSentiment/blob/master/vaderSentiment/vaderSentiment.py
        # despite is in negative sentiment list
        self.negate = ["aint", "arent", "cannot", "cant",
                       "couldnt", "darent", "didnt", "doesnt",
                       "ain't", "aren't", "can't", "couldn't",
                       "daren't", "didn't", "doesn't",
                       "dont", "hadnt", "hasnt", "havent",
                       "isnt", "mightnt", "mustnt", "neither",
                       "don't", "hadn't", "hasn't", "haven't",
                       "isn't", "mightn't", "mustn't",
                       "neednt", "needn't", "never", "none",
                       "nope", "nor", "not", "nothing", "nowhere",
                       "oughtnt", "shant", "shouldnt", "uhuh",
                       "wasnt", "werent", "oughtn't", "shan't",
                       "shouldn't", "uh-uh", "wasn't", "weren't",
                       "without", "wont", "wouldnt", "won't", "wouldn't",
                       "rarely", "seldom", "despite"]
        self.cap_negate = [w.upper() for w in self.negate]
