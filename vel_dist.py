import math
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import maxwell

# Abrimos el fichero temp para consultar los datos finales de la simulacion
filepath = '/home/willy/Documentos/codigo_git/clone_pyMD/results/temp.dat'
with open(filepath, 'r') as f:
    for line in f.readlines():
        pass
    last_line = line.split()
    # Leemos la temperatura en 'equilibrio'
    T = 0.5*float(last_line[0])

# Ruta donde se guardan los archivos .dat
ruta = '/home/willy/Documentos/codigo_git/clone_pyMD/results'
# Leemos nombres de los archivos y contamos cuantos
# 'frames' hay
npart = 25  # Particulas simuladas
names = os.listdir(ruta)
count = [1 if 'vxvy' in name else 0 for name in names]
count = np.array(count)
total_frames = np.sum(count)
vels = np.zeros((total_frames, npart))  
vels_vect = np.zeros((npart*total_frames, 2))  # Para guardar los vectores velocidad

# Para el histograma
bins = 25
vmax = 7
vmin = 0
data_hist = np.zeros((total_frames, bins))
average = np.zeros(bins)

for i in range(total_frames):
    filename = f'vxvy{i:04d}.dat'
    # Ruta del archivo con las velocidades
    frame = os.path.join(ruta, filename)
    # Leemos las velocidades y calculamos el modulo
    dat = open(frame)
    j = 0
    for pos in dat.readlines():
        splitted = pos.split()
        coords = (float(splitted[0]), float(splitted[1]))
        vels_vect[i+j][0] = coords[0]
        vels_vect[i+j][1] = coords[1]
        mod = np.sqrt(coords[0]**2 + coords[1]**2) 
        vels[i][j] = mod
        j = j + 1
    dat.close()

    # Guardamos la frecuencia de cada barra del histograma
    counts, intervals = np.histogram(vels[i], bins=bins, range=(vmin, vmax), density=True)
    data_hist[i] = counts
    average = average + data_hist[i]

# Histograma medio
average = average/total_frames

# Densidad original
m = 1
kB = 1
maxwell_og = lambda v: (m*v/(kB*T))*np.exp(-(m*v**2)/(2*kB*T))

x = np.linspace(0.01, 7, 100)
#plt.plot(x, maxwell.pdf(x), lw=3, label='Maxwell Distr')
plt.plot(x, maxwell_og(x), lw=3, label='Maxwell pers.')
plt.stairs(average, intervals, color='brown', alpha=0.7, fill=True, label='Resultados sim.')
plt.legend()
plt.savefig('vel_dist.png')
#plt.show()

# Momentos
meas = npart*total_frames  # Total mediciones de la velocidad
first_mom = [0,0]
for vect in vels_vect:
    first_mom = first_mom + vect
first_mom = first_mom/meas
print('El primer momento de la velocidad es: ', first_mom)

sec_mom = [0,0]
for vect in vels_vect:
    sec_mom[0] = sec_mom[0] + (vect[0]-first_mom[0])**2
    sec_mom[1] = sec_mom[1] + (vect[1]-first_mom[1])**2
sec_mom = sec_mom/meas
print('El segundo momento de la velocidad es: ', sec_mom)

third_mom = [0,0]
for vect in vels_vect:
    third_mom[0] = third_mom[0] + (vect[0]-first_mom[0])**3
    third_mom[1] = third_mom[1] + (vect[1]-first_mom[0])**3
third_mom[0] = third_mom[0]/(meas*np.sqrt(sec_mom[0])**3)
third_mom[1] = third_mom[1]/(meas*np.sqrt(sec_mom[1])**3)
print('El tercer momento de la velocidad es: ', third_mom)

fourth_mom = [0,0]
for vect in vels_vect:
    fourth_mom[0] = fourth_mom[0] + (vect[0]-first_mom[0])**4
    fourth_mom[1] = fourth_mom[1] + (vect[1]-first_mom[1])**4
fourth_mom[0] = fourth_mom[0]/(meas*sec_mom[0]**2)
fourth_mom[1] = fourth_mom[1]/(meas*sec_mom[1]**2)
print('El cuarto momento de la velocidad es: ', fourth_mom)
