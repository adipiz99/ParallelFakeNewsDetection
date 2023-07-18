import os

proc_num = '8'

#windows
os.execvp('mpiexec', ['mpiexec', '-np', proc_num, 'python', 'deepq_simulation.py'])