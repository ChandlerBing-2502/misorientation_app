# symmetry_operators.py
import numpy as np

def get_cubic_symmetry_operators():
    """Return 24 rotation matrices representing cubic crystal symmetry."""
    ops = []

    # Identity
    I = np.identity(3)
    ops.append(I)

    # 90, 180, 270 deg rotations around x, y, z
    R = lambda axis, theta: np.round(np.array([
        [np.cos(theta) + axis[0]**2 * (1 - np.cos(theta)),
         axis[0]*axis[1]*(1 - np.cos(theta)) - axis[2]*np.sin(theta),
         axis[0]*axis[2]*(1 - np.cos(theta)) + axis[1]*np.sin(theta)],
        [axis[1]*axis[0]*(1 - np.cos(theta)) + axis[2]*np.sin(theta),
         np.cos(theta) + axis[1]**2 * (1 - np.cos(theta)),
         axis[1]*axis[2]*(1 - np.cos(theta)) - axis[0]*np.sin(theta)],
        [axis[2]*axis[0]*(1 - np.cos(theta)) - axis[1]*np.sin(theta),
         axis[2]*axis[1]*(1 - np.cos(theta)) + axis[0]*np.sin(theta),
         np.cos(theta) + axis[2]**2 * (1 - np.cos(theta))]
    ]), 6)

    angles = [np.pi/2, np.pi, 3*np.pi/2]
    axes = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]

    for axis in axes:
        for angle in angles:
            ops.append(R(axis, angle))

    # Add 180-degree rotations about face diagonals
    diagonals = [
        np.array([1, 1, 0]), np.array([1, -1, 0]),
        np.array([1, 0, 1]), np.array([1, 0, -1]),
        np.array([0, 1, 1]), np.array([0, 1, -1])
    ]
    for d in diagonals:
        d = d / np.linalg.norm(d)
        ops.append(R(d, np.pi))

    # Add 120-degree rotations about body diagonals
    body_diagonals = [
        np.array([1, 1, 1]), np.array([-1, 1, 1]),
        np.array([1, -1, 1]), np.array([1, 1, -1])
    ]
    for bd in body_diagonals:
        bd = bd / np.linalg.norm(bd)
        ops.append(R(bd, 2*np.pi/3))  # 120°
        ops.append(R(bd, 4*np.pi/3))  # 240°

    return ops
