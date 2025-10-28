import KJV as k

index = 0
user = input('Book: ')

for index, value in enumerate(k.bible['books']):
    if value['name'] == user:
        for i in range(len(k.bible['books'][index]['chapters'])):
            book = k.bible['books'][index]['name']
            chapter = k.bible['books'][index]['chapters'][i]['chapter']
            for verses in k.bible['books'][index]['chapters'][i]['verses']:
                verse = verses['verse']
                print(f"{book} {chapter}:{verse}")
                print(verses['text'])
    index+=1

