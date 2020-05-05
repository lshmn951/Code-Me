import time
from crawler import bojcrawler
import database_management as dm


def get_user_accept_proportion(uid):
    """유저의 실제 승률 푼문제/(못푼문제+푼문제)"""
    solved_probs = dm.select_user_solved_problem(uid)
    failed_probs = dm.select_user_failed_problem(uid)
    proportion = 0.0
    if len(solved_probs) > 0:
        proportion = len(solved_probs) / (len(solved_probs)+len(failed_probs))
    return proportion


def start_user_rating(uid):
    """유저의 rating이 0 일때 rating 값 계산"""
    prob_list = dm.select_user_solved_problem(uid)
    count_dict = dm.select_count_return_dict()
    probs = list(prob_list)
    rating = 0.00
    for pb in prob_list:
        tp = []
        for pr in probs:
            if pb != pr and pr in count_dict and count_dict[pr][pr - 1000] != 0 and pr-1000 < 17000 and pb-1000<17000:
                tp.append(count_dict[pr][pb - 1000] / count_dict[pr][pr - 1000])
        if len(tp)>0:
            rating = rating + 40 * (1-max(tp))
        print(rating)
    return round(rating,3)


def get_new_accept_problem(uid):
    """디비에 저장된 푼문제와 크롤링한 푼문제가 다르면 새롭게 푼문제로 판단하고 리턴"""
    prob_list = bojcrawler.get_accept_list_by_user(uid)
    new_probs = list(prob_list)
    solved_probs = dm.select_user_solved_problem(uid)
    for prob in solved_probs:
        new_probs.remove(prob)
    return prob_list, new_probs


def plus_user_rating(prob_list, new_probs):
    """새롭게 푼 문제들의 승률 계산해서 리스트로 리턴"""
    count_dict = dm.select_count_return_dict()
    plus=[]
    for new in new_probs:
        tp = []
        for pr in prob_list:
            if new != pr and pr in count_dict and count_dict[pr][pr-1000] != 0 and pr-1000 < 17000 and new-1000<17000:
                tp.append(count_dict[pr][new-1000]/count_dict[pr][pr-1000])
        if len(tp) > 0:
            plus.append(max(tp))
    return plus


def get_user_rating(uid):
    """유저의 rating이 0 이면 새롭게 계산해서 리턴
        0이 아니면 새롭게 푼문제들의 승률을 바탕으로 기존 rating에 더함"""
    prob_list, new_probs = get_new_accept_problem(uid)
    user_rating = dm.select_user_rating(uid)
    if user_rating == 0 :
        user_rating = start_user_rating(uid)
    else :
        plus = plus_user_rating(prob_list, new_probs)
        for pl in plus:
            user_rating = user_rating + 40 * (1 - pl)
    return round(user_rating,3)



"""
if __name__ == '__main__':
    #count = 1
    cd = dm.select_count_return_dict()
    #ul = dm.select_user_name_list()

    for user in ul:
        if str(user[1]) < "2019-11-10 00:00:00" :
            print(count)
            print(user[0])
            rt = start_user_rating(user[0],cd)
            dm.update_user_rating_to_database(rt,user[0])
        count = count + 1

    rt = start_user_rating("rinny99",cd)
    dm.update_user_rating_to_database(rt,"rinny99")"""