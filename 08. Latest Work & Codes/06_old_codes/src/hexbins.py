import numpy as np
import matplotlib.pyplot as ax
hexes = ax.hexbin()

def get_hexlines(v, h, m):
    """
    Function that returns line coordinates for a hexagon
    given the midpoint of the hexagon.
    
    Args:
        v (float): vertical distance from the center.
        h (float): horizontal distance from the center.
        m (numpy.ndarray): array containing center-coordinates of a hexagon.
        
    Returns:
        numpy.ndarray: containing line coordinates of a hexagon.
    """
    # init hexagon coordinates template array --> clockwise direction
    hex_coord = np.array(
        [
            [ [0, v], [h, v / 2] ],         # first line
            
            [ [h, v / 2], [h, -v / 2] ],    # second line
            
            [ [h, -v / 2], [0, -v] ],       # third line
             
            [ [-h, -v/2], [0, -v] ],        # fourth line
            
            [ [-h, v / 2], [-h, -v / 2] ],  # fifth line
            
            [ [0, v], [-h, v/2] ]           # sixth line
        ]
    )
    
    return hex_coord + m

# get midpoints of hexagons
midpoints = hexes.get_offsets()

# get count for each hexagons
hex_count = hexes.get_array()

# get only those hexagons where count is greater than some number
selected_hex = midpoints[hex_count >= 3]

# vertical distance from the center  (array of distance-values)
dis_vertical = (midpoints[1:, 1] - midpoints[:-1, 1]) / 3       # the number 3 is manually chosen as per the size of hexagon

# horizontal distance from the center (array of distance-values)
dis_horizontal = (midpoints[1:, 0] - midpoints[:-1, 0]) / 2     # the number 2 is manually chosen as per the size of hexagon

# pick only one distance value
dis_vertical = dis_vertical[dis_vertical > 0][0]
dis_horizontal = dis_horizontal[dis_horizontal > 0][0]

# get hexagon line coordinates
lines_coord = np.concatenate(
    [get_hexlines(dis_vertical, dis_horizontal, center) for center in selected_hex]
)

# get all the unique lines with thier counts
unique_lines, count = np.unique(lines_coord.round(1), axis=0, return_counts=True)

# final coordinate whose count is 1 (i.e. unique line coordinates)
final_coords = unique_lines[count == 1]

# plot lines
for line_coord in final_coords:
    ax.plot(
        line_coord[:, 0], line_coord[:, 1], color="#F2F2F2",
        lw=1.5, zorder=3
    )