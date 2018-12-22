# -*- coding: utf-8 -*-

# quick and fun code that plots a christmas tree

import matplotlib.pyplot as plt
import numpy as np


# star:
def star(size):
    p1_x = 0
    p1_y = size

    p2_x = size*np.tan(np.radians(18))
    p2_y = 0

    p3_y = np.sin(np.radians(36)) * size/np.cos(np.radians(18))
    p3_x = np.cos(np.radians(36)) * size/np.cos(np.radians(18))
    p3_x = -(p3_x - p2_x)

    p4_y = p3_y
    p4_x = -p3_x

    p5_x = -p2_x
    p5_y = p2_y

    xs = np.array([p1_x, p2_x, p3_x, p4_x, p5_x, p1_x])
    ys = np.array([p1_y, p2_y, p3_y, p4_y, p5_y, p1_y])

    return xs, ys


star_xs, star_ys = star(1.2)


# body:
b_xs = [[0]]
b_ys = [[0]]

width = 15

for i in range(width):
    x = np.random.uniform(low=-i*0.5, high=i*0.5, size=i*3)
    y = np.full(len(x), -i)
    b_xs.append(x)
    b_ys.append(y)

body_xs = np.concatenate(b_xs)
body_ys = np.concatenate(b_ys)


# trunk:
t_xs = []
t_ys = []

for i in range(width, width+5):
    x = np.random.uniform(low=-2, high=2, size=15)
    y = np.full(len(x), -i)
    t_xs.append(x)
    t_ys.append(y)

trunk_xs = np.concatenate(t_xs)
trunk_ys = np.concatenate(t_ys)


# connection:
conn_xs = np.concatenate((b_xs[-1], t_xs[0]))
conn_ys = np.concatenate((b_ys[-1], t_ys[0]))


###############################################################################
# plot:
fig, ax = plt.subplots(figsize=(9,9))

alpha = 0.3
ax.plot(star_xs, star_ys, color='white', alpha=0.5)
ax.scatter(star_xs, star_ys, color='grey', edgecolor='white', s=3)

ax.triplot(conn_xs, conn_ys, color='white', alpha=alpha)
ax.triplot(body_xs, body_ys, color='white', alpha=alpha)
ax.triplot(trunk_xs, trunk_ys, color='white', alpha=alpha)

ax.scatter(body_xs, body_ys, color='grey', edgecolor='white')
ax.scatter(trunk_xs, trunk_ys, color='grey', edgecolor='white')

ax.set_xlim(left=-17, right=17)

ax.patch.set_facecolor('black')

plt.axis('equal')
plt.savefig('tree.jpg', dpi=400, bbox_inches='tight', pad_inches=0)
