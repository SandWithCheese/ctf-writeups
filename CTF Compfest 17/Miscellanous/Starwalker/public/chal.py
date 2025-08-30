#!/usr/local/bin/python3.12
import base64
import io
from contextlib import redirect_stdout, redirect_stderr
from dis import _all_opmap as op

banner = """
                            @@                               
                          @@@@@                              
                          @@  @@                             
                        @@@    @@                            
                        @@     @@@                           
                       @@        @@                          
                     @@            @@                        
                @@@@@@@@@@@@@@       @@                      
           @@@@@    @    @@@@@@@@@@@@@@@@@                   
        @@@           @       @  @@@  @@@@@@@@@@             
           @@@@         @@@@@           @    @@@@@@@@        
              @@@@@@                                @@@@@@@@@
                   @@                               @@@@@@@@@
                   @@                        @@@@@@@@        
                   @@         @@@          @@@@@             
                   @@         @@@          @@                
                 @@@        @@ @@        @@@                 
                 @@@        @@ @@       @@                   
                 @@@       @@  @@       @@                   
                @@         @@@@@      @@                     
                @@       @@  @@       @@                     
                @@      @@@  @@      @@@                     
              @@       @@    @@      @@                      
              @@      @@    @@       @@                      
             @@       @@    @@     @@                        
            @@@       @@  @@@      @@                        
   @@@@@@@@@@       @@    @@       @@                        
 @@@                @@    @@       @@                        
@@                @@@   @@       @@@@@@@@@                   
@@@@@@@@@@@@@@@@@@@@    @@               @@@                 
@@@@@@@@@@@@@@@@@@    @@                 @@@                 
                      @@@@@@@@@@@@@@@@@@@@        

These birds are Pissing me off...           
"""

# I'll ban both opcodes AND opargs >:)
banned_bytes = [
    'IMPORT_NAME', 'IMPORT_FROM', 'GET_ITER', 
    'FOR_ITER', 'FOR_ITER_LIST', 'FOR_ITER_TUPLE', 'FOR_ITER_RANGE',
    'BINARY_SUBSCR', 'STORE_SUBSCR', 'DELETE_SUBSCR',
    'EXTENDED_ARG', 'POP_TOP', 'POP_EXCEPT',
    'CALL', 'CALL_NO_KW_BUILTIN_FAST', 'CALL_NO_KW_STR_1',
]

# No LOAD and STORE for you
for o in op.keys():
    if o.startswith("LOAD") or o.startswith("STORE"):
        banned_bytes.append(o)

def f(): pass

def get_stdout(f):
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        safe = globals().copy()
        safe['__builtins__'] = {'print': print}
        eval(f.__code__, safe, safe)
    return out.getvalue().strip()

def print_flag():
    with open('./flag.txt') as f:
        print(f'Heres the    flag: {f.read()}')

def good(s):
    return 50 <= len(s) <= 100 and sum([x for x in s]) % 17 == 0 and all([op[i] not in map(int, s) for i in banned_bytes])

print(banner)

try:
    code = base64.b64decode(input('>>> '))
except:
    print('This base64 is Pissing me off...')
    exit() 

if not good(code):
    print('These characters are Pissing me off...')
    exit()

f.__code__ = f.__code__.replace(co_code=code, co_consts=(), co_names=())
out = get_stdout(f)
if str(out) == str(code):
    print_flag()
else:
    print('No')