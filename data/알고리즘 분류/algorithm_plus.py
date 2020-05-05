import pandas as pd
import csv

algo_list = []
prob_list = []


with open('algorithm_problems.csv',"r",encoding = 'cp949') as file :
    csv_reader = csv.reader(file,delimiter=',')
    for row in csv_reader:
        algo_list.append(row)


with open('problems_list.csv',"r",encoding='utf-8') as file:
    csv_reader = csv.reader(file,delimiter='\t')
    for row in csv_reader:
        prob_list.append(row)


for algo in algo_list:
    for algo_prob in algo[1:-1]:
        for prob in prob_list:
            if prob[0] == algo_prob:
                if not prob[-1] :
                    prob[-1] = algo[0]


with open('new_problem_list.csv',"w",encoding='utf-8',newline='') as file:
    writer = csv.writer(file,delimiter='\t')
    writer.writerows(prob_list)