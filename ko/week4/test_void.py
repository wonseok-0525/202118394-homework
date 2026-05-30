import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111, projection='3d')

# Box
r = [0, 40]
for s, e in combinations(np.array(list(product(r, [0, 30], [0, 15]))), 2):
    if np.sum(np.abs(s-e)) in [40, 30, 15]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='--', alpha=0.3)

# Apple centers
x_centers = np.linspace(5, 35, 4)
y_centers = np.linspace(5, 25, 3)
z_centers = np.linspace(3.75, 11.25, 2)
CX, CY, CZ = np.meshgrid(x_centers, y_centers, z_centers)
cx = CX.flatten()
cy = CY.flatten()
cz = CZ.flatten()

# Scatter apples
ax1.scatter(cx, cy, cz, s=800, c='#FF5252', alpha=1.0, edgecolors='#B71C1C')

# Generate void points
resolution = 1.5 # cm
vx, vy, vz = np.meshgrid(np.arange(0, 40, resolution), 
                         np.arange(0, 30, resolution), 
                         np.arange(0, 15, resolution))

# Radius threshold
radius = 3.5
pts = np.vstack([vx.flatten(), vy.flatten(), vz.flatten()]).T
centers = np.vstack([cx, cy, cz]).T

# Calculate distance from all points to all centers
# Shape: (N_pts, 1, 3) - (1, N_centers, 3) -> (N_pts, N_centers, 3)
# Quick distance check:
from scipy.spatial import cKDTree
tree = cKDTree(centers)
distances, _ = tree.query(pts)

# Void points are those where distance to nearest center > radius
void_mask = distances > radius
void_pts = pts[void_mask]

# Plot voids
# Sample down void points for performance and visual clarity
sub_sample = int(len(void_pts) * 0.2)
idx = np.random.choice(len(void_pts), sub_sample, replace=False)
v_pts_sub = void_pts[idx]

ax1.scatter(v_pts_sub[:,0], v_pts_sub[:,1], v_pts_sub[:,2], s=10, c='red', alpha=0.1, marker='s')

ax1.set_box_aspect((40, 30, 15))
plt.savefig("test_void.png")
