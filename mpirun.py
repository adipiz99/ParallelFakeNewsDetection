import os
#windows
os.execvp('mpiexec', ['mpiexec', '-np', '8', 'python', 'deepq_simulation.py'])