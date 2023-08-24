import os

proc_num = '13'
path = os.path.abspath('test/test_sa_1/parallel_test.py')

#windows
#os.execvp('mpiexec', ['mpiexec', '-np', proc_num, 'python', path])

#linux
os.execvp('mpirun', ['mpirun', '-np', proc_num, 'python', path])