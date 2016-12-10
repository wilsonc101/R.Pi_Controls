import time


i = 3
while True:
    while i % 2:
	i = int(time.strftime("%M"))
        print(str(i % 2))
        print(i)
        time.sleep(3)

