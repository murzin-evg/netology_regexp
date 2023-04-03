import csv
import re


def regexp_file(data: list):
    result_data = [data[0],]

    for row in data[1:]:
        pattern = r'(\w+)[ |,](\w+)[ |,](\w+)?,+(\w+)?,+([^,]+)?,+((8|\+7)\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(?[доб.]*\s*(\d*)\)?)?,([\w\.-]*@?\w*\.?[a-zA-Z]{2,3})?'
        subst = r'\1,\2,\3,\4,\5,\6,\13'
        
        temp = re.sub(
            pattern=pattern,
            repl=subst,
            string=','.join(row)
        )
        
        temp = re.split(',', temp)

        for i in result_data:
            if i[:2] == temp[:2]:
                for index_j, j in enumerate(i):
                    if j == '' and temp[index_j] != '':
                        i[index_j] = temp[index_j]

                break
        else:
            result_data.append(temp)
    
    return result_data

def regexp_phone(data: list):
    pattern = r'(8|\+7)\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(?[доб.]*\s*(\d*)\)?'
    subst1 = r'+7(\2)\3-\4-\5 доб. \6'
    subst2 = r'+7(\2)\3-\4-\5'

    for row in data:

        if row[5] is None:
            continue
        elif 'доб.' in row[5]:
            row[5] = re.sub(pattern=pattern, repl=subst1, string=row[5])
        else:
            row[5] = re.sub(pattern=pattern, repl=subst2, string=row[5])

    return data


if __name__ == '__main__':

    with open('phonebook_raw.csv', 'r', newline='', encoding='utf-8') as f:
        data = list(csv.reader(f, delimiter=','))

    filter_data = regexp_file(data)
    res = regexp_phone(filter_data)

    with open('phonebook_raw_FILTER.csv', 'w', newline='', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(res)

