import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_camera_origins(R, T):
    # Define the camera positions
    camera_1_position = np.array([0, 0, 0])
    camera_2_position = -R.T @ T.squeeze()

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the camera origins
    ax.scatter(*camera_1_position, color='red', label='Camera 1 Origin')
    ax.scatter(*camera_2_position, color='blue', label='Camera 2 Origin')

    # Plot the coordinate axes for camera 1
    ax.quiver(0, 0, 0, 1000, 0, 0, color='red', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1000, 0, color='green', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1000, color='blue', arrow_length_ratio=0.1)

    # Plot the coordinate axes for camera 2
    x_axis = R @ np.array([1000, 0, 0]) + camera_2_position
    y_axis = R @ np.array([0, 1000, 0]) + camera_2_position
    z_axis = R @ np.array([0, 0, 1000]) + camera_2_position
    ax.quiver(*camera_2_position, *x_axis-camera_2_position, color='red', arrow_length_ratio=0.1)
    ax.quiver(*camera_2_position, *y_axis-camera_2_position, color='green', arrow_length_ratio=0.1)
    ax.quiver(*camera_2_position, *z_axis-camera_2_position, color='blue', arrow_length_ratio=0.1)


    # Set the axis labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-1000, 1000)
    ax.set_ylim(-1000, 1000)
    ax.set_zlim(-1000, 1000)

    # Add a legend
    ax.legend()

    # Show the plot
    plt.show()
R = np.array([[ 0.9938163,   0.09601568, -0.05576873],
 [-0.00515206 , 0.54158827,  0.8406281 ],
 [ 0.11091717, -0.83514259 , 0.53873393]])
T = np.array([ 0,
646.1538223038002,
0])

plot_camera_origins(R, T)
