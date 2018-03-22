import numpy as np


def initial_velocity(positions, dt):
    return np.gradient(positions, dt, axis=0)


def trajectory_per_frame(positions, fps):
    epsilon = 0.0000001 * positions[0,1]
    dt = np.true_divide(1.0, fps)
    v = initial_velocity(positions, dt)[1]
    next_position = np.copy(positions[-1, :])
    trajectory = np.asarray([next_position, ])
    acceleration = np.array([0,-980,0])
    while next_position[1] > epsilon:
        next_position += v * dt
        v += acceleration * dt
        trajectory = np.r_[trajectory, next_position]
    if trajectory[-1, 1] < 0:
        trajectory[-1, 1] = 0
    return trajectory


def calculate_rotation(normal, reverse=False):
    phi = np.arccos(np.dot(normal, [0,1,0]))
    rotation_matrix = np.array([[np.cos(phi),0,-np.sin(phi)],[0,1,0],
                                [np.sin(phi),0,np.cos(phi)]])
    if reverse:
        return np.linalg.inv(rotation_matrix)
    else:
        return rotation_matrix


def rotate_frame(positions, normal):
    rotation = calculate_rotation(normal, False)
    return np.einsum('ij,kj',rotation,positions)


def rotate_trajectory(trajectory, normal):
    rotation = calculate_rotation(normal, True)
    return np.einsum('ij,kj',rotation,trajectory)



def find_trajectory(positions, normal, fps):
    rot_pos = rotate_frame(positions, normal)
    return trajectory_per_frame(rot_pos, fps)
