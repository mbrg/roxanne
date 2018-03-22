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
    while next_position[1] >= epsilon:
        next_position += v * dt
        v += acceleration * dt
        trajectory = np.r_[trajectory, next_position.reshape((1, 3))]
    if trajectory[-1, 1] < 0:
        trajectory[-1, 1] = 0
    return trajectory


def rotate_frame(positions, normal):
    phi = np.arccos(np.dot(normal, [0,1,0]))
    rotation_matrix = np.array([[np.cos(phi),0,-np.sin(phi)],
                                [0,1,0],
                                [np.sin(phi),0,np.cos(phi)]])
    rotated_positions = np.asarray([[0, 0, 0], ])
    for row in positions:
        rotated_positions = np.r_[rotated_positions, np.matmul(rotation_matrix, row).reshape((1, 3))]
    return rotated_positions[1:, :]


def find_trajectory(positions, normal, fps):
    rot_pos = rotate_frame(positions, normal)
    return trajectory_per_frame(rot_pos, fps)