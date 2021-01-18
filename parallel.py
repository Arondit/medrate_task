from concurrent import futures
import os

from script import main, transaction

MAX_WORKERS = 20
def parallel_process(users, todos):
    workers = min(len(users), MAX_WORKERS)
    if not os.path.isdir("tasks"):
        os.mkdir("tasks")
    with futures.ThreadPoolExecutor(workers) as executor:
        for user in users: 
            user_todos = [t for t in todos if t['userId']==user['id']]
            executor.submit(transaction, user=user, todos=user_todos)

main(process=parallel_process, is_check_needed=True, show_time=True)