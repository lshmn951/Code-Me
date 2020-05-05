import csv
import database_management as dm


def read_counting_from_csv():
    count_list = []
    with open('count.csv',"r") as file :
        csv_reader = csv.reader(file)
        for row in csv_reader:
            temp_list=[]
            for tp in row:
                temp_list.append(int(tp))
            count_list.append(temp_list)
    print("finish")
    return count_list


def read_algorithm_from_csv():
    algo_list = []
    with open('algorithm_problems_sojung.csv',"r") as file :
        csv_reader = csv.reader(file)
        for row in csv_reader:
            temp_list = []
            temp_list.append(row[0])
            for tp in row[1:]:
                if tp.isdigit():
                    temp_list.append(int(tp))
            algo_list.append(temp_list)
    return algo_list


def counting_to_database(count_list):
    conn,cur = dm.connect_database()
    problem_list = dm.select_problem_number()
    for prob in problem_list:
        st = ""
        tp = prob[0]-999
        print(prob[0])
        if tp < len(count_list):
            st = st + str(count_list[tp])
            st = st.replace("[", "'{")
            st = st.replace("]", "}'")
            cur.execute(f"insert into tb_problem_counting(problem_id,count_array) values({prob[0]},{st})")

    conn.commit()

    return cur.close(), conn.close()


conn, cur = dm.connect_database()
ra = read_algorithm_from_csv()
for a in ra[::-1]:
    temp = dm.select_algorithm_one(a[0])
    print(temp)
    for tp in a[1:]:
        q = tp
        cur.execute(f"update tb_problem set algorithm_id_id = {temp} where number = {tp}")
        print(tp)
conn.commit()
cur.close()
conn.close()