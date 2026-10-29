import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cbook
from matplotlib.colors import LightSource

# Load and format data
dem = cbook.get_sample_data('jacksboro_fault_dem.npz')
z = dem['elevation']
nrows, ncols = z.shape
x = np.linspace(dem['xmin'], dem['xmax'], ncols)
y = np.linspace(dem['ymin'], dem['ymax'], nrows)
x, y = np.meshgrid(x, y)

region = np.s_[5:50, 5:50]
x, y, z = x[region], y[region], z[region]



grad_row , grad_col = np.gradient(z)

row , col = 10.0, 30.0
l_r = 0.05
iter = 300
path = [(row, col)]

for it in range(iter):
    i = int(round(row))
    j = int(round(col))

    g_row = grad_row[i,j]
    g_col = grad_col[i,j]

    row = row - g_row * l_r
    col = col - g_col * l_r

    path.append((row, col))

path = np.array(path)
print(f'شروع: {z[int(path[0][0]), int(path[0][1])]}')
print(f'پایان: {z[int(path[-1][0]), int(path[-1][1])]}')

rows_idx = np.round(path[:, 0]).astype(int)
cols_idx = np.round(path[:, 1]).astype(int)

path_x = x[rows_idx, cols_idx]
path_y = y[rows_idx, cols_idx]
path_z = z[rows_idx, cols_idx] + 15



fig, ax = plt.subplots(subplot_kw=dict(projection='3d', computed_zorder=False))

ls = LightSource(270, 45)
rgb = ls.shade(z, cmap=plt.colormaps["gist_earth"], vert_exag=0.1, blend_mode='soft')
ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                linewidth=0, antialiased=False, shade=False, zorder=1)

ax.plot(path_x, path_y, path_z,  color='red', markersize=10, linewidth=2, zorder=10)
ax.scatter(path_x[0], path_y[0], path_z[0], color='blue', s=150, zorder=11)
ax.scatter(path_x[-1], path_y[-1], path_z[-1], color='red', s=150, zorder=11)

ax.view_init(elev=50, azim=-120)

ax.legend()
plt.savefig('ball_result.png', dpi=120)
plt.show()


