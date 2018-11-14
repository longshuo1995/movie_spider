from app.db_master import mongo
from app.spider import spider_94a1


def judge(mvs):
    return len(mvs)


def get_mvs(keyword):
    # 查询数据库
    mvs = [i for i in mongo.search(keyword)]
    if not judge(mvs):
        mvs = spider_94a1.get_mvs(keyword)
        mongo.insert(mvs)
    return mvs


if __name__ == '__main__':
    res = get_mvs("阿凡达")
    print(res)
