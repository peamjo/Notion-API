import schedule
import time

def foo():
    print("Fooing around")

start = time.time()
#schedule.every().day.at("03:00").do(foo)
end = time.time()

print(f"Time taken to run the code was {end-start} seconds")

#update box office gross
#update people's Dates
