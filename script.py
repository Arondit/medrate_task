import os 
import json
from collections import defaultdict
import datetime
import time

import requests

def get_text(user, todos):
    today = datetime.datetime.today()
    def stringfy_titles(tt): 
        return  '\n'.join([t['title'] for t in tt])
    completed = [t for t in todos if t['completed'] is True]
    not_completed = [t for t in todos if t['completed'] is False]
    result = f"""Отчёт для {user['company']['name']}.
{user['name']} <{user['email']}> {today.strftime("%d.%m.%Y %H:%M")}
Всего задач: {len(todos)}"""
    if len(todos):
        result+=f"""

Завершённые задачи ({len(completed)}):
{stringfy_titles(completed)}

Оставшиеся задачи ({len(not_completed)}):
{stringfy_titles(not_completed)}"""
    return result


def transaction(user, todos):
    try: 
        user_text = get_text(user, todos)
    except KeyError: pass
    else:
        if not os.path.isdir("program_data"):
            os.mkdir("program_data")
        with open(f'program_data/new_{user["username"]}.txt', 'w') as f:
            f.write(user_text)
        save_new_report(user['username'])
        #time.sleep(1) # Чтобы лучше была видна эффективность параллельной версии

def save_new_report(username):      
    if os.path.isfile(f'program_data/new_{username}.txt'):
        old_dir = f'program_data/new_{username}.txt'
        new_dir = f'tasks/{username}.txt'
        if os.path.isfile(f'tasks/{username}.txt'):
            with open(f'tasks/{username}.txt', 'r') as f:
                f.readline()
                old_date = f.readline()
                date_start = old_date.find('>')+2
                old_date = old_date[date_start:date_start+16]
                old_date = datetime.datetime.strptime(old_date+':00', "%d.%m.%Y %H:%M:%S")  
                old_name = f'tasks/{username}.txt'
                new_name = f'tasks/old_{username}_{old_date.strftime("%Y-%m-%dT%H:%M")}.txt'   
            if os.path.isfile(new_name): 
                point = new_name.find('.txt')
                os.rename(old_name, new_name[:point]+'_v2'+new_name[point:])
            else: 
                os.rename(old_name, new_name)
        os.replace(old_dir, new_dir)

def cons_process(users, todos):
    if not os.path.isdir("tasks"):
        os.mkdir("tasks")
    for user in users: 
        user_todos = [t for t in todos if t['userId']==user['id']]
        transaction(user, user_todos)
        
def get_data():
    users_response = requests.get('https://json.medrating.org/users')
    todos_response = requests.get('https://json.medrating.org/todos')
    users = json.loads(users_response.content.decode())
    todos = json.loads(todos_response.content.decode())
    todos = [defaultdict(lambda: -1, t) for t in todos]
    return [users, todos]

def is_file_correct(name):
    with open(name,'r') as f:
        lines = f.readlines()
        if len(lines)<3: return False
        if len(lines)==3: return True
        left_bracket = lines[2].find(':')
        n = int(lines[2][left_bracket+2:])
        if len(lines)<n+7: return False #если строк меньше, чем количество задач + 7, то заполнение файла прервалось 
    return True

def check_last_end():
    if os.path.isdir('program_data'):
        for file_name in os.listdir('program_data'):
            if  is_file_correct('program_data/'+file_name):
                save_new_report(file_name[4:len(file_name)-4])
            else: 
                os.remove('program_data/'+file_name)
                print('not correct file deleted from program_data: '+file_name)
    return True

def main(get=get_data, process=cons_process, is_check_needed=False, show_time = False): #по умолчанию никакой проверки корректного завершения не происходит
    global_start_time = time.time()
    if is_check_needed: check_last_end()
    try:
        data = get()
    except requests.exceptions.ConnectionError: 
        print("Something is wrong with connection")
    except requests.exceptions.HTTPError:
        print('Data not found')
    else:
        process_start_time = time.time()
        process(*data)
        if show_time:
            print(f'Process have been working for {time.time()-process_start_time} секунд')
            print(f'Script have been working for {time.time()-global_start_time} секунд')

if __name__=='__main__':
    main(get_data, cons_process, True, True)