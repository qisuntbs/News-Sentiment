#!/cygdrive/c/Users/qisun/Anaconda3/python

# This is the main file for the sentiment calucation
# from Shapio, Sudhof, and Wilson (2020)
# (LM + HL lexicons) words counts + negation

import time
from nltk import word_tokenize, tokenize
from func import lexi
from sample_txt import txt


def get_lexi():
    lex = lexi()
    return lex


def calc(sample_txt):
    sample = sample_txt
    lex = get_lexi()
    # split into sentences:
    sentences = tokenize.sent_tokenize(sample)
    p_carry = 0
    n_carry = 0
    token_len = 0
    for sen in sentences:
        tokens = word_tokenize(sen)
        sen_len = len(tokens)  # length of the tokens in the sentence
        token_len += sen_len  # length of ALL the tokens
        negate_indi = [0] * sen_len
        alnum_indi = [0] * sen_len
        for i in range(sen_len):
            alnum_indi[i] = int(tokens[i].isalnum())
            negate_indi[i] = int(tokens[i] in lex.cap_negate)
            if i == 0:
                indi = 0
            elif i <= 3:
                # indi for negate within the last 3 words
                indi = sum(negate_indi[0:i]) % 2
            else:  # i > 3
                n = 3
                while (i > n) and (sum(alnum_indi[i-n:i]) != 3):
                    n += 1
                indi = sum(negate_indi[i-n:i]) % 2
            if (tokens[i] in lex.positive) & (not indi):
                # print("positive token and NO negation:", tokens[i])
                p_carry += 1
            elif (tokens[i] in lex.positive) & indi:
                # print("positive token and NEGATION:", tokens[i])
                n_carry += 1
            elif (tokens[i] in lex.negative) & (not indi):
                # print("negative token and NO negation:", tokens[i])
                n_carry += 1
            elif (tokens[i] in lex.negative) & indi:
                # print("negative token and NEGATION:", tokens[i])
                p_carry += 1
        # print("positive counts:", p_carry)
        # print("negative counts:", n_carry)
        # print('-----------------------------')

    # for negate in lex.negate:
    #     if negate.upper() in lex.negative:
    #         print("negate in lex.negative:", negate)  # DESPITE
    #     elif negate.upper() in lex.positive:
    #         print("negate in lex.positive:", negate)

    # print("p_carry", p_carry)
    # print("n_carry", n_carry)
    # print("len(tokens)", token_len)
    # return (p_carry/token_len - n_carry/token_len), tokens, lex
    if p_carry + n_carry == 0:
        score = 0
    else:
        score = (p_carry - n_carry)/(p_carry + n_carry)
    if abs(score) < 0.1:
        if score > 0:
            adj_score = 0.1
        elif score < 0:
            adj_score = -0.1
        else:
            adj_score = 0
    else:
        adj_score = round(score*10)/10
    return adj_score, tokens, lex


if __name__ == "__main__":
    t = time.time()
    sample_txt = txt()
    out, tokens, lex = calc(sample_txt)
    out = round(out, 4)
    if out > 0:
        print("POSITIVE:", out)
    elif out < 0:
        print("NEGATIVE:", out)
    elif out == 0:
        print("NEUTRAL ARTICAL")

    print(time.time() - t, 'seconds taken.')
