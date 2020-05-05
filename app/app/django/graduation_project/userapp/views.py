from django.shortcuts import render
from django.utils import timezone

from .models import (
    User,
    Problem,
    UserSolvedProblem,
    UserFailedProblem,
    ProblemCounting,
)

from .crawler import bojcrawler
import psycopg2
import json


ENVFILE_PATH = '/home/ec2-user/app/django/graduation_project/graduation_project/envdata.json'


def user_search_index(request):
    return render(request, 'userapp/index.html')


def user_search(request):
    uname = request.GET.get('username')

    try:
        uinfo = User.objects.get(name=uname)
        time_gap = (timezone.localtime() - uinfo.last_update)
        
        if time_gap.days > 0 or time_gap.seconds > 300:
            user_update(uname)
            uinfo = User.objects.get(name=uname)
            time_gap = (timezone.localtime() - uinfo.last_update)
        
        urank = User.objects.filter(rating__gt=uinfo.rating).count() + 1
        uinfo.rating = round(uinfo.rating)

        tusplist = UserSolvedProblem.objects.filter(user=uname)
        usplist = [(usprob.problem_id, Problem.objects.get(number=usprob.problem_id).name) for usprob in tusplist]

        tufplist = UserFailedProblem.objects.filter(user=uname)
        ufplist = [(ufprob.problem_id, Problem.objects.get(number=ufprob.problem_id).name) for ufprob in tufplist]

        ureno = user_recommend(uname)

        html_template = 'userapp/user.html'
        context = {
            'user_info': uinfo,
            'user_rank': urank,
            'user_solved_problem_list': usplist,
            'user_failed_problem_list': ufplist,
            'time_gap': str(time_gap),
            'user_recommend': ureno,
        }
    except User.DoesNotExist:
        html_template = 'userapp/user_not_found.html'
        context = {}

    return render(request, html_template, context)


def ttee():
    print('test')


def user_update(username):
    slist = bojcrawler.get_solved_list_by_user(username)
    flist = bojcrawler.get_failed_list_by_user(username)

    tusplist = UserSolvedProblem.objects.filter(user=username)
    usplist = [usprob.problem_id for usprob in tusplist]

    tufplist = UserFailedProblem.objects.filter(user=username)
    ufplist = [ufprob.problem_id for ufprob in tufplist]

    update_sset = set(slist) - set(usplist)
    update_fset = set(flist) - set(ufplist)

    with open(ENVFILE_PATH, 'rt', encoding='utf-8') as fi:
        envdata = json.loads(fi.read())

    with psycopg2.connect(
        dbname=envdata['DB_NAME'],
        user=envdata['DB_USER'],
        password=envdata['DB_PASSWORD'],
        host=envdata['DB_HOST'],
    ) as conn:
        conn.set_session(autocommit=True)

        with conn.cursor() as cur:
            if update_sset:
                for update_s in update_sset:
                    cur.execute(f"insert into tb_user_solved_problem(problem_id, user_id) values ({update_s}, '{username}')")

            if update_fset:
                for update_f in update_fset:
                    cur.execute(f"insert into tb_user_failed_problem(problem_id, user_id) values ({update_f}, '{username}')")

            cur.execute(f"update tb_user set last_update=now() where name='{username}'")


def user_recommend(username):
    tusplist = UserSolvedProblem.objects.filter(user=username)

    if len(tusplist) == 0:
        recommend_number = 1000
    else:
        usplist = [tusp.problem_id for tusp in tusplist]
        tmparr = []
        for ind, usp in enumerate(usplist):
            pidpc = ProblemCounting.objects.get(problem=usp).count_array
            pivot = pidpc[usp - 1000]
            if pivot == 0 or usp -1000 == ind: continue
            else:
                for i in range(len(pidpc)):
                    pidpc[i] = pidpc[i] / pivot
            tmparr.append([usp,pidpc])
        resarr = []
        maxnum = 0
        for i in range(0,17000):
            for prob_num in range(len(tmparr)):
                if tmparr[prob_num][1][i] > maxnum and i+1000 not in usplist:
                    maxnum = tmparr[prob_num][1][i]
            resarr.append(maxnum)
        minnum = 1
        for i in range(0,17000):
            if abs(0.8 - resarr[i]) < minnum and i + 1000 not in usplist:
                recommend_num = i + 1000
                minnum = abs(0.8 -resarr[i])
        return recommend_num

