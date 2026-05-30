import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111, projection='3d')

r = [0, 40]
for s, e in combinations(np.array(list(product(r, [0, 30], [0, 15]))), 2):
    if np.sum(np.abs(s-e)) in [40, 30, 15]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='--', alpha=0.3)

x_centers = np.linspace(4, 36, 5)
y_centers = np.linspace(5, 25, 3)
z_centers = np.linspace(2.5, 12.5, 3)
X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers)

ax1.scatter(X, Y, Z, s=600, c='#8BC34A', alpha=0.9, edgecolors='#33691E')

# --- 공극(Void) 시각화 ---
res = 1.5
vx, vy, vz = np.meshgrid(np.arange(0, 40, res), np.arange(0, 30, res), np.arange(0, 15, res))
pts = np.vstack([vx.flatten(), vy.flatten(), vz.flatten()]).T
centers = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).T

diff = pts[:, np.newaxis, :] - centers[np.newaxis, :, :] 
distances = np.linalg.norm(diff, axis=-1) 
min_distances = np.min(distances, axis=1) 

void_mask = min_distances > 3.0
void_pts = pts[void_mask]

sub_sample_size = int(len(void_pts) * 0.8)  # Increase sampling to 80%
if sub_sample_size > 0:
    idx = np.random.choice(len(void_pts), sub_sample_size, replace=False)
    v_pts_sub = void_pts[idx]
    ax1.scatter(v_pts_sub[:,0], v_pts_sub[:,1], v_pts_sub[:,2], 
                s=40, c='#FF0000', alpha=0.3, marker='s', edgecolors='none')  # Larger, more opaque

ax1.set_box_aspect((40, 30, 15))
plt.savefig("test_void_numpy.png")
