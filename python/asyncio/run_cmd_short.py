import os
#import sys
import time
import platform
import asyncio
async def run_command(*args):
    """Run command in subprocess
    
    Example from:
        http://asyncio.readthedocs.io/en/latest/subprocess.html
    """
    # Create subprocess
    global glbl
    glbl=args[0]
    b_stdinw = len(args) >= 3
    if b_stdinw:        
        if args[-2] is None :
            stdinw=args[-1]
            args=args[0:-2]
            glbl=stdinw    

    process = await asyncio.create_subprocess_exec(
        *args,
        # stdout must a pipe to be accessible as process.stdout
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    if b_stdinw:
        process.stdin.write(stdinw.encode(encoding='utf-8'))
        process.stdin.close()
    
    # Status
    print('Started:', args, '(pid = ' + str(process.pid) + ')')

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    
    print('Done:', args, '(pid = ' + str(process.pid) + ')')    
    # Progress
    if process.returncode == 0:
        pass        
    else:
        print('Failed:', args, '(pid = ' + str(process.pid) + ')')
        # Result
        with open("os_command.py.log","a") as f:
            f.write(datetime.now().strftime("%Y%m%d %H:%m:%S"))
            f.write(stderr.decode().strip())
        
    
    # Return stdout
    try:
        return process.returncode,stdout.decode().strip(),stderr.decode().strip()
    except:
        return process.returncode  
def main(commands=[]):
    start = time.time()
    
    if len(commands)==0:
        if platform.system() == 'Windows':
            # Commands to be executed on Windows
            commands = [
                ["python","read_stdin.py",None,"a\n東京都\nc"],["pwd"],["hostname"]
            ]
        else:
            # Commands to be executed on Unix
            commands = [
                ['du', '-sh', '/var/tmp'],
                ['hostname'],
            ]
    
    tasks = []
    for command in commands:
        tasks.append(run_command(*command))

    all_results = []
    if platform.system() == 'Windows':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    g_commands = asyncio.gather(*tasks)  # Unpack list using *
    results = loop.run_until_complete(g_commands)
    
    loop.close()
    print(f"commands: \n{commands}")
    print('Results:', results)

    end = time.time()
    rounded_end = ('{0:.4f}'.format(round(end-start,4)))
    print('Script ran in about', str(rounded_end), 'seconds')
    print(f"glbl:{glbl}")
'''
None 以降はstdinに書き込まれる。
'''
main(
    [
        ["python","read_stdin.py",None,"a\n東京都\nc"],
        ["pwd"],
        ["hostname"]
            ])
