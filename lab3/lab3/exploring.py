#!/usr/bin/env python3

# This assignment lets you both define a strategy for picking the next point to explore and determine how you
#  want to chop up a full path into way points. You'll need path_planning.py as well (for calculating the paths)
#
# Note that there isn't a "right" answer for either of these. This is (mostly) a light-weight way to check
#  your code for obvious problems before trying it in ROS. It's set up to make it easy to download a map and
#  try some robot starting/ending points
#
# Given to you:
#   Image handling
#   plotting
#   Some structure for keeping/changing waypoints and converting to/from the map to the robot's coordinate space
#
# Slides

# The ever-present numpy
import numpy as np
import os

# Your path planning code
try:
    import lab3.path_planning as path_planning
except:
    import path_planning as path_planning


# -------------- Showing start and end and path ---------------
def plot_with_explore_points(im_threshhold, zoom=1.0, robot_loc=None, explore_points=None, best_pt=None):
    """Show the map plus, optionally, the robot location and points marked as ones to explore/use as end-points
    @param im - the image of the SLAM map
    @param im_threshhold - the image of the SLAM map
    @param robot_loc - the location of the robot in pixel coordinates
    @param best_pt - The best explore point (tuple, i,j)
    @param explore_points - the proposed places to explore, as a list"""

    # Putting this in here to avoid messing up ROS
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 1)
    axs.imshow(im_threshhold, origin='lower', cmap="gist_gray")
    axs.set_title("threshold image")

    # Show original and thresholded image
    if explore_points is not None:
        for p in explore_points:
            axs.plot(p[0], p[1], '.b', markersize=2)

    if robot_loc is not None:
        axs.plot(robot_loc[0], robot_loc[1], '+r', markersize=10)
    if best_pt is not None:
        axs.plot(best_pt[0], best_pt[1], '*y', markersize=10)
    axs.axis('equal')

    # Implements a zoom - set zoom to 1.0 if no zoom
    width = im_threshhold.shape[1]
    height = im_threshhold.shape[0]

    axs.set_xlim(width / 2 - zoom * width / 2, width / 2 + zoom * width / 2)
    axs.set_ylim(height / 2 - zoom * height / 2, height / 2 + zoom * height / 2)


# -------------- For converting to the map and back ---------------
def convert_pix_to_x_y(im_size, pix, size_pix):
    """Convert a pixel location [0..W-1, 0..H-1] to a map location (see slides)
    Note: Checks if pix is valid (in map)
    @param im_size - width, height of image
    @param pix - tuple with i, j in [0..W-1, 0..H-1]
    @param size_pix - size of pixel in meters
    @return x,y """
    if not (0 <= pix[0] <= im_size[1]) or not (0 <= pix[1] <= im_size[0]):
        raise ValueError(f"Pixel {pix} not in image, image size {im_size}")

    return [size_pix * pix[i] / im_size[1-i] for i in range(0, 2)]


def convert_x_y_to_pix(im_size, x_y, size_pix):
    """Convert a map location to a pixel location [0..W-1, 0..H-1] in the image/map
    Note: Checks if x_y is valid (in map)
    @param im_size - width, height of image
    @param x_y - tuple with x,y in meters
    @param size_pix - size of pixel in meters
    @return i, j (integers) """
    pix = [int(x_y[i] * im_size[1-i] / size_pix) for i in range(0, 2)]

    if not (0 <= pix[0] <= im_size[1]) or not (0 <= pix[1] <= im_size[0]):
        raise ValueError(f"Loc {x_y} not in image, image size {im_size}")
    return pix


def is_reachable(im, pix):
    """ Is the pixel reachable, i.e., has a neighbor that is free?
    Used for
    @param im - the image
    @param pix - the pixel i,j"""

    # GUIDE: Returns True (the pixel is adjacent to a pixel that is free)
    #  False otherwise
    # You can use four or eight connected - eight will return more points
    # YOUR CODE HERE

    for nbr in path_planning.eight_connected(pix):
        x, y = nbr
        if 0 <= x < im.shape[1] and 0 <= y < im.shape[0]:
            if path_planning.is_free(im, nbr):
                return True
    return False


def find_all_possible_goals(im):
    """ Find all of the places where you have a pixel that is unseen next to a pixel that is free
    It is probably easier to do this, THEN cull it down to some reasonable places to try
    This is because of noise in the map - there may be some isolated pixels
    @param im - thresholded image
    @return list of possible pixel (x,y) locations"""

    # YOUR CODE HERE

    possible_points = []
    filter_threshold = 10 # this is a filter for selecting high-quality pixels to send to Dijkstra early.
    # lower == more noise, more data.
    # higher == less noise, less data.
    # find a good middle ground! 
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            pt = (x, y)
            if path_planning.is_unseen(im, pt) and is_reachable(im, pt):
            # Hey you! Don't delete this yet!! README! - MD
            # we added a density check here!
                point_neighborhood = im[y-2:y+3, x-2:x+3] 
                unseen_points_in_neighborhood = (point_neighborhood == 128) # filter for where points are actually unseen (==128)
                number_of_unseen_points = np.sum(unseen_points_in_neighborhood) # now sum how many of those points exist in the 5x5 square around pt = (x,y)
                # now use this as a conditional:
                if number_of_unseen_points >= filter_threshold:
                    possible_points.append(pt)
                # - MD
                


    # IMPORTANT NOTE RE: CULLING:
    # there is a cheap and stupid way to handle this:
    # possible_points = possible_points[0,-1, 10]
    # just return every 10th point... 
    # ... However Dijkstra is EXPENSIVE--if we prune here, we will have a much faster
    # ... path-planning algorithm. There might
    return possible_points
    


def find_best_point(im, possible_points : list, robot_loc):
    """ Pick one of the unseen points to go to
    @param im - thresholded image
    @param possible_points - possible points to chose from (list of tuples)
    @param robot_loc - location of the robot (in case you want to factor that in)
    """
    # YOUR CODE HERE

    best_pt = None
    best_score = None

    for pt in possible_points:
        count_free = 0
        count_unseen = 0
        free_neighbors = []

        for ix in range(-1, 2):
            for iy in range(-1, 2):
                nbr = (pt[0] + ix, pt[1] + iy)
                if 0 <= nbr[0] < im.shape[1] and 0 <= nbr[1] < im.shape[0]:
                    if path_planning.is_free(im, nbr):
                        count_free += 1
                        free_neighbors.append(nbr)
                    elif path_planning.is_unseen(im, nbr):
                        count_unseen += 1

        if count_free >= 3 and (count_free + count_unseen == 9):
            dist = np.sqrt((pt[0] - robot_loc[0])**2 + (pt[1] - robot_loc[1])**2)
            score = (-count_free, dist)

            if best_score is None or score < best_score:
                best_score = score

                best_pt = min(
                    free_neighbors,
                    key=lambda nbr: np.sqrt((nbr[0] - robot_loc[0])**2 + (nbr[1] - robot_loc[1])**2)
                )

    if best_pt is None and len(possible_points) > 0:
        for pt in sorted(possible_points,
                        key=lambda p: np.sqrt((p[0] - robot_loc[0])**2 + (p[1] - robot_loc[1])**2)):
            free_neighbors = []
            for ix in range(-1, 2):
                for iy in range(-1, 2):
                    nbr = (pt[0] + ix, pt[1] + iy)
                    if 0 <= nbr[0] < im.shape[1] and 0 <= nbr[1] < im.shape[0]:
                        if path_planning.is_free(im, nbr):
                            free_neighbors.append(nbr)
            if free_neighbors:
                best_pt = min(
                    free_neighbors,
                    key=lambda nbr: np.sqrt((nbr[0] - robot_loc[0])**2 + (nbr[1] - robot_loc[1])**2)
                )
                break

    return best_pt


def find_waypoints(im, path):
    """ Place waypoints along the path
    @param im - the thresholded image
    @param path - the initial path
    @ return - a new path"""

    # Again, no right answer here
    # YOUR CODE HERE

    if path is None or len(path) == 0:
        return []

    if len(path) <= 10:
        return path

    n_waypoints = 8
    indices = np.linspace(0, len(path) - 1, n_waypoints, dtype=int)

    new_path = []
    last_pt = None
    for idx in indices:
        pt = path[idx]
        if pt != last_pt:
            new_path.append(pt)
            last_pt = pt

    if new_path[-1] != path[-1]:
        new_path.append(path[-1])

    return new_path


def test_unseen(im, pts):
    for pt in pts:
        count_free = 0
        count_unseen = 0
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                if path_planning.is_free(im, (pt[0] + ix, pt[1] + iy)):
                    count_free += 1
                elif path_planning.is_unseen(im, (pt[0] + ix, pt[1] + iy)):
                    count_unseen += 1
        if count_free == 0 or count_unseen == 0:
            return False
    return True


def test_best(im, pt):
    """ Check that the selected point has at least 3 free neighbors"""
    count_free = 0
    count_unseen = 0
    for ix in range(-1, 2):
        for iy in range(-1, 2):
            if path_planning.is_free(im, (pt[0] + ix, pt[1] + iy)):
                count_free += 1
            elif path_planning.is_unseen(im, (pt[0] + ix, pt[1] + iy)):
                count_unseen += 1
    if count_free < 3:
        return False
    if count_free + count_unseen != 9:
        return False
    return True


if __name__ == '__main__':
    _, im_thresh = path_planning.open_image("map.pgm")

    robot_start_loc = (60, 40)

    all_unseen = find_all_possible_goals(im_thresh)
    best_unseen = find_best_point(im_thresh, all_unseen, robot_loc=robot_start_loc)

    assert test_unseen(im=im_thresh, pts=all_unseen)
    assert test_best(im=im_thresh, pt=best_unseen)

    plot_with_explore_points(im_thresh, zoom=1.0, robot_loc=robot_start_loc, explore_points=all_unseen, best_pt=best_unseen)

    path = path_planning.dijkstra(im_thresh, robot_start_loc, best_unseen)
    waypoints = find_waypoints(im_thresh, path)
    path_planning.plot_with_path(im_thresh, zoom=1.0, robot_loc=robot_start_loc, goal_loc=best_unseen, path=waypoints)

    # Depending on if your mac, windows, linux, and if interactive is true, you may need to call this to get the plt
    # windows to show
    # Putting this in here to avoid messing up ROS
    import matplotlib.pyplot as plt
    plt.show()

    print("Done")