import pinyin
import jieba
import string
import re


def construct_dict(file_path):
    word_freq = {}
    with open(file_path, "r") as f:
        for line in f:
            info = line.split()
            word = info[0]
            frequency = info[1]
            word_freq[word] = frequency

    return word_freq


def load_cn_words_dict(file_path):
    cn_words_dict = ""
    with open(file_path, "r") as f:
        for word in f:
            cn_words_dict += word.strip()
    return cn_words_dict


def edits1(phrase, cn_words_dict):
    "All edits that are one edit away from `phrase`."
    phrase = phrase
    splits = [(phrase[:i], phrase[i:]) for i in range(len(phrase) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in cn_words_dict]
    if '呕吐' in replaces:
        print('---')
    inserts = [L + c + R for L, R in splits for c in cn_words_dict]
    return set(deletes + transposes + replaces + inserts)


filename = r'/Users/haojingkun/Downloads/bert_for_corrector /rule_error/token_freq_pos%40350k_jieba.txt'
phrase_freq = construct_dict(filename)


def known(phrases):
    result = set()
    for phrase in phrases:
        if phrase in phrase_freq:
            result.add(phrase)
    result = list(result)
    return result


def get_candidates(error_phrase):
    candidates_1st_order = []
    candidates_2nd_order = []
    candidates_3nd_order = []

    error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/").encode("utf-8")
    error_pinyin = str(error_pinyin, encoding='utf-8')
    cn_words_dict = load_cn_words_dict("/Users/haojingkun/Downloads/bert_for_corrector /rule_error/cn_dict.txt")
    candidate_phrases = list(known(edits1(error_phrase, cn_words_dict)))

    for candidate_phrase in candidate_phrases:
        candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/").encode("utf-8")
        candidate_pinyin = str(candidate_pinyin, encoding='utf-8')
        if candidate_pinyin == error_pinyin:
            candidates_1st_order.append(candidate_phrase)
        elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
            candidates_2nd_order.append(candidate_phrase)
        else:
            candidates_3nd_order.append(candidate_phrase)

    return candidates_1st_order, candidates_2nd_order, candidates_3nd_order


def auto_correct(error_phrase):
    # 按照出现频次排序
    c1_order, c2_order, c3_order = get_candidates(error_phrase)
    # print c1_order, c2_order, c3_order
    if c1_order:
        return max(c1_order, key=phrase_freq.get)
    elif c2_order:
        return max(c2_order, key=phrase_freq.get)
    else:
        return max(c3_order, key=phrase_freq.get)


error_phrase_1 = "呕涂"  # should be "呕吐"
error_phrase_2 = "东方之朱"  # should be "东方之珠"
error_phrase_3 = "沙拢"  # should be "沙龙"

print(error_phrase_1, auto_correct(error_phrase_1))
print(error_phrase_2, auto_correct(error_phrase_2))
print(error_phrase_3, auto_correct(error_phrase_3))
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）"


def auto_correct_sentence(error_sentence, verbose=True):
    jieba_cut = jieba.cut(error_sentence, cut_all=False)
    seg_list = "\t".join(jieba_cut).split("\t")

    correct_sentence = ""

    for phrase in seg_list:

        correct_phrase = phrase
        # check if item is a punctuation
        if phrase not in PUNCTUATION_LIST:
            # check if the phrase in our dict, if not then it is a misspelled phrase
            if phrase not in phrase_freq.keys():
                correct_phrase = auto_correct(phrase)
                if verbose:
                    print(phrase, correct_phrase)

        correct_sentence += correct_phrase

    if verbose:
        print(correct_sentence)
    return correct_sentence


err_sent = '机七学习是人工智能领遇最能体现智能的一个分知！'
correct_sent = auto_correct_sentence(err_sent)
