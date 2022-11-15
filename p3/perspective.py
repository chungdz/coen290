import pandas as pd
from utilities import project_to_img

# Read files
vertices = pd.read_csv('face-vertices.data', header=None, names=['x', 'y', 'z'])
indices = pd.read_csv('face-index.txt', header=None, names=['p1', 'p2', 'p3'])

# image settings
offset = 600
scale_factor = 1000

# recale and move the points
perspective_df = vertices.apply(lambda row: [int(row['x'] * scale_factor) + offset, 
                                             int(row['y'] * scale_factor) + offset, 
                                             int(row['z'] * scale_factor) + offset], axis=1, result_type='expand')
perspective_df.rename(columns={0: 'x', 1: 'y', 2: 'z'}, inplace=True)

# draw images from different angles with two mode
xy = project_to_img(perspective_df[['x', 'y']])
xy.save('xy_points_only.jpg')
yz = project_to_img(perspective_df[['y', 'z']])
yz.save('yz_points_only.jpg')
xz = project_to_img(perspective_df[['x', 'z']])
xz.save('xz_points_only.jpg')

xy = project_to_img(perspective_df[['x', 'y']], indices=indices)
xy.save('xy_trangles.jpg')
yz = project_to_img(perspective_df[['y', 'z']], indices=indices)
yz.save('yz_trangles.jpg')
xz = project_to_img(perspective_df[['x', 'z']], indices=indices)
xz.save('xz_trangles.jpg')




