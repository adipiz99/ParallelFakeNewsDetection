import os

proc_num = '8'
path = os.path.abspath('test/test_sa_3/parallel_test_3.py')

#windows
#os.execvp('mpiexec', ['mpiexec', '-np', proc_num, 'python', path])

#linux
os.execvp('mpirun', ['mpirun', '-np', proc_num, 'python', path])