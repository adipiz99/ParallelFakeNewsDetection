import os

proc_num = '8'
path = os.path.abspath('test/test_sa_5/parallel_test_5.py')

#windows
os.execvp('mpiexec', ['mpiexec', '-np', proc_num, 'python', path])