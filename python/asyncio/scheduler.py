#if not hasattr(cls,'schedule'):
        
import asyncio
from datetime import datetime as dt

class Task:
    schedule=[]
    @classmethod
    async def main(cls):
        pass        
    @classmethod
    def sub(cls):
        if len(cls.schedule)==0 or not len(cls.schedule[-1])==0:
            cls.schedule.data.append([])
        return cls
class Task1(Task):
    pass
class Task1(Task):
    pass
class Scheduler:    
    def __init__(self,task_dic):
        self.task_dic=task_dic
    @classmethod
    async def exec_if(cls,T):
        if cls.eval_schedule(T.schedule):
            await T.main()
    @classmethod
    async def eval_schedule(cls,sch):
        for subsch in sch:
            for item in subsch:
                if getattr(cls,f"eval_{item[0]}")(item[1:]):return True
        return False
def main(scheduler):
    if platform.system() == 'Windows':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    
    T_main=[ Scheduler.exec_if(T)  for T in Scheduler.tasks]
    g_commands = asyncio.gather(*T_main) 
    results = loop.run_until_complete(g_commands)
    
    loop.close()
    
    print('Results:', results)

    end = time.time()
#############################################

#############################################
sch=Scheduler()
sch.tasks=[Task1,Task2]
Task1.sub().nfind(Task1.id).at("21:00",every=10,until="23:45")
Task1.sub().nfind(Task1.id).at("21:30",every=5,until="00:30")
Task2.sub().find(Task1.id).at("21:30",every=5,until="00:30")

#############################################

main(sch)