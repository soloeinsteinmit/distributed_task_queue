import time

from celery.result import AsyncResult

from worker import random_number, app

time.sleep(5)

result_future = random_number.delay(100) # this is used to submit the task. so because of the task decorator, the delay can be called as a method of the random_number function and the arguement is passed. in this eg. 100
result = AsyncResult(result_future.id, app=app)

print("Submitted task")

print(result.state)

while True:
    if result.ready():
        print(result.get())
        break
    else:
        print(result.state)
        time.sleep(1)