import time
import psycopg2


def connect_database():
    conn_string = "host=grad-db.cbqy6xvaiqrp.ap-northeast-2.rds.amazonaws.com dbname=graduationdb \
     user=gradpostgre password=dlawhdlqor200 port=5432"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    return conn,cur


def update_user_rating_to_database(user_rating,uid):
    conn, cur = connect_database()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    cur.execute(f"update tb_user set rating = {user_rating}, last_update = '{now}' where name = '{uid}'")
    conn.commit()
    return cur.close(),conn.close()


def insert_user_to_database(user_rating,uid):
    conn, cur = connect_database()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    cur.execute(f"insert into tb_user(name,rating,last_update) values ('{uid}',{user_rating},'{now}')")
    conn.commit()
    return cur.close(), conn.close()


def select_user_solved_problem(uid):
    conn, cur = connect_database()
    cur.execute(f"select problem_id from tb_user_solved_problem where user_id = '{uid}'")
    solved_probs = cur.fetchall()
    sl = []
    for sp in solved_probs:
        sl.append(sp[0])
    cur.close()
    conn.close()
    return sl


def select_user_failed_problem(uid):
    conn, cur = connect_database()
    cur.execute(f"select problem_id from tb_user_failed_problem where user_id = '{uid}'")
    failed_probs = cur.fetchall()
    fl = []
    for fp in failed_probs:
        fl.append(fp[0])
    cur.close()
    conn.close()
    return fl


def select_problem_number():
    conn, cur = connect_database()
    cur.execute("select number from tb_problem")
    problem_list = cur.fetchall()
    cur.close()
    conn.close()
    return problem_list


def select_count_return_dict():
    conn, cur = connect_database()
    cur.execute("select * from tb_problem_counting")
    counting = cur.fetchall()
    dic = {}
    for c in counting:
        dic[c[0]] = c[1]
    cur.close()
    conn.close()
    return dic


def select_user_rating(uid):
    conn, cur = connect_database()
    cur.execute(f"select rating from tb_user where name = '{uid}'")
    user_rating = cur.fetchall()
    cur.close()
    conn.close()
    if user_rating :
        return user_rating[0][0]
    else :
        return None


def select_algorithm(algo):
    conn, cur = connect_database()
    cur.execute(f"select * from tb_algorithm")
    algo = cur.fetchall()
    cur.close()
    conn.close()
    return algo


def select_algorithm_id(name):
    conn, cur = connect_database()
    cur.execute(f"select algorithm_id from tb_algorithm where name = '{name}'")
    na = cur.fetchone()
    cur.close()
    conn.close()
    return na[0]


def select_user_name_list():
    conn, cur = connect_database()
    cur.execute("select name from tb_user")
    ul = cur.fetchall()
    cur.close()
    conn.close()
    return ul


