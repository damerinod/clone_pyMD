import os
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy as np

# Función para calcular la distancia euclídea entre 2 puntos
def euc_dist(x,y):
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)

R = 1
diam = 2*R
npart = 25
# Ruta donde se guardan los archivos .dat
ruta = '/home/willy/Documentos/codigo_git/clone_pyMD/results'
# Leemos nombres de los archivos y contamos cuantos
# 'frames' hay
names = os.listdir(ruta)
count = [1 if 'xy' in name else 0 for name in names]
count = np.array(count)
total_frames = np.sum(count)

# Para el histograma
diag = math.sqrt(50**2 + 50**2)  
dmax = diag-diam
dr = 0.05
bins = np.arange(0,dmax,dr)
data_hist = np.zeros((total_frames, len(bins)-1))
average = np.zeros((len(bins)-1))
denom = 2*np.pi*bins[1:]

# En cada frame calcularemos el histograma de distancias
for i in range(total_frames):
    filename = f'xy{i:04d}.dat'
    frame = os.path.join(ruta, filename)
    dists = []
    with open(frame, 'r') as f:
        lines = f.readlines()
        L = len(lines)
        for j in range(L):
            splitted1 = lines[j].split()
            p = (float(splitted1[0]), float(splitted1[1]))
            for k in range(j+1, L):
                splitted2 = lines[k].split()
                q = (float(splitted2[0]), float(splitted2[1]))
                d = euc_dist(p,q)
                dists.append(d/2)
    
    counts, intervals = np.histogram(dists, bins=bins, range=(0,dmax))
    # Dividimos la cantidad de distancia a cierto R, entre R
    data_hist[i] = counts/denom
    average = average + data_hist[i]

# Histograma medio y representamos
pmax = 60
x_ax = np.arange(0,pmax,1)
mid_points = bins[:-1]
average = average/total_frames
plt.xticks(x_ax)
plt.yticks([])
plt.xlabel(r'r/$\sigma$')
plt.ylabel('g(r)')
plt.plot(mid_points[:pmax], average[:pmax], marker='*')
plt.savefig('rad_dist.png')
plt.show()