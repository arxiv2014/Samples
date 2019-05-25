import asyncio
from datetime import datetime as dt

async def f(name, number):
    now1=dt.now()
    for i in range(number+5):
        time_past=(dt.now()-now1).seconds
        print(f"Task {name}: {time_past} seconds past")
        await asyncio.sleep(number)
    now2=dt.now()
    return f"{name}:{(now2-now1).seconds} seconds spent"
async def main():
    now1=dt.now()
    #.strftime("%S")
    commands = asyncio.gather(
        f("A", 3),
        f("B", 2),
        f("C", 1),
    )
    await commands
    print("{}".format(commands))
    now2=dt.now()
    print(f"main:{(now2-now1).seconds} seconds spent")
asyncio.run(main())