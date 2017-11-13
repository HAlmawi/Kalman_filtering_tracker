import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Appends data points to list for plotting
# Input: int x, int y, int z, int list x_points, int list y_points, int list z_points
# Output: updated int lists: int list x_points, int list y_points, int list z_points
def combine_datapoints(x,y,z,x_points,y_points,z_points):
    x_points.insert(len(x_points),x)
    y_points.insert(len(y_points),y)
    z_points.insert(len(z_points),z)
    return x_points, y_points, z_points

# Plots the points on a scatter plot and returns a figure
# Input: int list x_points, int list y_points, int list z_points
# Output: scatter plot figure
def plot_points(x_points, y_points, z_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    return ax