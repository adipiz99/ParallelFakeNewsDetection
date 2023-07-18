import os

proc_num = '8'
path = os.path.abspath('test/test_sa_4/parallel_test_4.py')

#windows
os.execvp('mpiexec', ['mpiexec', '-np', proc_num, 'python', path])