from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db_movie = conn.wechat_movie
mov_collection = db_movie.movie


def search(key_word):
    key_word = key_word.replace(' ', ' ')
    key_words = key_word.split()
    # 搜索导演：
    director_pattern = '^.*'+'.*'.join(key_words) + '.*$'
    director_result = mov_collection.find({'director': {'$regex': director_pattern}})

    # search title
    search_pattern = '^.?'+'.*'.join(key_words) + '.?$'
    search_query = {
        'title': {'$regex': search_pattern},
        'title': {'$regex': '^.*{%s,%s}$' % (len(key_word), len(key_word)*2)}}
    title_result = mov_collection.find(search_query)
    director_result = [i for i in director_result]
    title_result = [i for i in title_result]
    return director_result + title_result


def search_play_detail(_id):
    res = mov_collection.find_one({'_id': _id})
    return res


def insert(mvs):
    for mv in mvs:
        try:
            mov_collection.insert_one(mv)
        except:
            pass
