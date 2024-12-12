with open("test3.txt.txt", "r",encoding='utf-8') as f:
    with open("test.txt", "w",encoding='utf-8') as f2:
        for line in f:
            f2.write(line.replace('<p>','').replace('</p>', '').replace('<br>', '').replace('</br>', ''))
            f2.write('\n')