#python shell, default import 
#https://stackoverflow.com/questions/1350887/python-is-there-a-place-when-i-can-put-default-imports-for-all-my-modules
#https://qiita.com/ognek/items/a37dd1cd0e26e6adecaa
import psycopg2,sys
from datetime import datetime
def get_conn():
    return psycopg2.connect("host=localhost port=5432 dbname=dKeyVal user=postgres password='##autidd'")

def check_duplicate(lines,skey0):
    row=lines[0]
    skey,cval=row.split(" ")    
    with get_conn() as conn:    
        with conn.cursor() as cur:
            cur.execute(f"select count(*) from tKeyVal where skey ='{skey}' and skey0 != '{skey0}';")
            (count,) = cur.fetchone()
            return count==0
        
def find(skey):
    with get_conn() as conn:
        #print(f"{conn.get_backend_pid()}")
        and_where_skey="" if skey=="*" else f" and skey like '%{skey}%' " 
        with conn.cursor() as cur:
            cur.execute(f"with t as (select skey,skey0,cval,cdate, last_value(cdate) over (partition by skey0 ORDER BY cdate RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as cdatel from tKeyVal ) select * from t where cdate=cdatel {and_where_skey};")
            for row in cur.fetchall():
                skey,skey0 ,cval,cdate,cdatel = row
                cdate=str(cdate).replace(" ","#")
                print(f"{skey} {skey0} {cdate} {cval}")
def insert(lines,skey0=None):
     with get_conn() as conn:
        #print(f"{conn.get_backend_pid()}")
        if skey0 is not None: 
            if len(lines) != 1:
                sys.stderr.write(f"from insrt:if skey0 is not None: assert len(lines) == 1 ,{len(lines)}\n {lines} \n")
                sys.exit(14)
        with conn.cursor() as cur:
            #default autocommit = False
            
            for row in lines:
                vals=row.split(" ")
                if len(vals)!=2:
                    sys.stderr.write(f"insert,for,if len(vals)!=2\n{row}\n")
                    sys.exit(11)
                skey,cval=vals
                skey=skey.strip()
                cval=cval.strip()
                skey0 = skey if skey0 is None else skey0
                cdate=datetime.now().strftime("%Y%m%d %H:%M:%S").strip()
                cur.execute(f"insert into tKeyVal(skey,skey0,cval,cdate) values('{skey}','{skey0}','{cval}','{cdate}');")
                if cur.rowcount!=1:
                    break                    
            else:
                conn.commit()                    
                sys.exit()    
            sys.stderr.write(f"rowcount:{cur.rowcount}\nlen(lines):{len(lines)}")
            sys.exit(12)
def pg_dump():
    import subprocess,os
    from datetime import datetime
    subprocess.check_call(["powershell",f"c:/Progra~1/PostgreSQL/11/bin/pg_dump.exe -h localhost -U postgres -p 5432 dKeyVal > log/dKeyVal.{datetime.now().strftime('%Y%m%d.%H%M%S')}.sql"])

if len(sys.argv)==1:
    sys.stderr.write("len(sys.argv)==1")
    sys.exit(10)
argv1=sys.argv[1] 
if "-pg_dump" in argv1:
    pg_dump()
if "-find" in argv1:
    find(sys.argv[2])
if "-insert" in argv1:
    insert(sys.stdin.readlines())    
if "-delete" in argv1:
    delete(sys.argv[2])
if "-update" in argv1:
    lines=sys.stdin.readlines()
    if not check_duplicate(lines,sys.argv[2]):
        sys.stderr.write("check_duplicate")
        sys.exit(13) 
    insert(lines,skey0=sys.argv[2])    

    
    


'''
    python -c 'from datetime import datetime as dt; print(dt.now().strftime("%Y%m%d %H:%M:%S"))'
'''
  