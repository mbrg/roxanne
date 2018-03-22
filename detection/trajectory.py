import numpy as np

def initial_velocity(positions, dt):
    return np.gradient(positions, dt, axis=0)


def trajectory_per_frame(positions, fps):
    epsilon = 0.0000001 * positions[0,1]
    dt = np.true_divide(1.0, fps)
    next_position = np.copy(positions[-1])
    v = initial_velocity(positions, dt)[1]
    trajectory = np.array([next_position])
    acceleration = np.array([0,-980,0])
    while next_position[1] > epsilon:
        next_position += v * dt
        v += acceleration * dt
        trajectory = np.append(trajectory, next_position)
    if trajectory[-1] < 0:
        trajectory[-1] = 0
    return np.reshape(trajectory, (int(np.floor(len(trajectory)/3)),3))

def rotate_frame(positions, normal):
    phi = np.arccos(np.dot(normal, [0,1,0]))
    rotation_matrix = np.array([[np.cos(phi),0,-np.sin(phi)],
                                [0,1,0],
                                [np.sin(phi),0,np.cos(phi)]])
    rotated_positions = np.asarray([])
    print(rotation_matrix)
    for row in positions:
        print(np.transpose(row))
        rotated_positions = np.append(rotated_positions, np.matmul(rotation_matrix, row))
    return np.reshape(rotated_positions,
     (int(np.floor(len(rotated_positions)/3)),3))