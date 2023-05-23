filename = r'/Users/haojingkun/Downloads/bert_for_corrector /renmin.txt'

target_filename = r'/Users/haojingkun/Downloads/bert_for_corrector /人民日报2009.txt'
target_w = open(target_filename, 'a+', encoding='utf-8')
with open(filename, 'r', encoding='utf-8') as data:
    lines = data.readlines()
    for line in lines:
        line = line.strip()
        texts = line.split(' ')
        sentence = ''
        for i in range(2, len(texts)):
            if texts[i] == '':
                continue
            sentence += texts[i].split('/')[0]
        if sentence == '' or len(sentence) < 7:
            continue
        sentence = sentence.replace('０', '0')
        sentence = sentence.replace('１', '1')
        sentence = sentence.replace('２', '2')
        sentence = sentence.replace('３', '3')
        sentence = sentence.replace('４', '4')
        sentence = sentence.replace('５', '5')
        sentence = sentence.replace('６', '6')
        sentence = sentence.replace('７', '7')
        sentence = sentence.replace('８', '8')
        sentence = sentence.replace('９', '9')
        target_w.write(sentence + '\n')
        print('----')
