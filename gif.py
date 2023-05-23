import os
import numpy as np
import matplotlib.pyplot as plt

# Ruta donde se guardan los archivos .dat
ruta = '/home/willy/Documentos/codigo_git/clone_pyMD/results'
# Leemos nombres de los archivos y contamos cuantos
# 'frames' hay
names = os.listdir(ruta)
count = [1 if 'xy' in name else 0 for name in names]
count = np.array(count)
total_frames = np.sum(count)
# Para representar hay activar el modo interactivo de venta (ion)
plt.ion()
# Creamos la ventana
fig = plt.figure()
for i in range(total_frames):
    # Creamos los ejes donde pintaremos las 10 esferas
    ax = fig.add_subplot(111)
    ax.set_xlim((-25, 25))
    ax.set_ylim((-25, 25))
    ax.axes.set_aspect('equal')
    filename = f'xy{i:04d}.dat'
    # Ruta del archivo con las posiciones
    frame = os.path.join(ruta, filename)
    # Leemos las posiciones y pintamos las esferas
    dat = open(frame)
    R = 1
    for pos in dat.readlines():
        splitted = pos.split()
        coords = (float(splitted[0]), float(splitted[1]))
        circle = plt.Circle(coords, 1, color='blue', fill=False)
        ax.add_patch(circle)
    dat.close()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.clf()
