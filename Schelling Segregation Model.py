from random import randrange

EMPTY = " "
BLUE = "."
ORANGE = "^"
NUM_TRIBES = 2
HOMOGENEITY_LOWER_BOUND = .333
HOMOGENEITY_UPPER_BOUND = 1

def print_world(world):
    world_size = len(world)
    print("  +" + (world_size * "-") + "+")
    for r, row in enumerate(world):
        line = str(r % 10) + " |"
        for col in row:
            line += col
        line += "|"
        print(line)
    print("  +" + (world_size * "-") + "+")
    print("   " + "".join(str(c % 10) for c in range(world_size)))

# find a random spot
def random_spot_finder(world, world_size, target):
    while True:
        rand_row = randrange(world_size)
        rand_col = randrange(world_size)
        if world[rand_row][rand_col] == target:
            return [rand_row, rand_col]

# want to check the ratio of neighbors:
#     if the neighbor is in the range, add one to total
#         how to test if it is in the range?
#         # if the actural col and row is in the world_size, then in the range
#         # loop through the index list to get the valid indexes
#         # loop through valid indexes:
#             if not empty, add one to total
#             if the neighbor is same as the target tribe, same_tribe_neighbor add one
#     give out the ratio
# if the target is a EMPTY: ratio = nothing ! let it equal to 0
# if the target is not empty
#     if it does not have a neighbor: ratio = 1
#     if it does hava neighbors: same_tribe / total
def ratio_checker(world, world_size, row, col):
    if world[row][col] == EMPTY:
        ratio = 0
    else:
        neighbors_indexes = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1], [row, col - 1], [row, col + 1],
                             [row + 1, col - 1], [row + 1, col], [row + 1, col + 1]]
        valid_neighbor = list(
            index for index in neighbors_indexes if 0 <= index[0] < world_size and 0 <= index[1] < world_size)
        total_neighbor = list(new_n for new_n in valid_neighbor if world[new_n[0]][new_n[1]] != EMPTY)
        if not total_neighbor:
            ratio = 1
        else:
            same_tribe_neighbor = list(new_n for new_n in total_neighbor if world[new_n[0]][new_n[1]] == world[row][col])
            ratio = len(same_tribe_neighbor) / len(total_neighbor)
    return ratio


# check if target is happy or not
#     if ratio is bigger than .333, happy, return Ture
#     else, unhappy return False
def satisfaction_check(world, world_size, row, col): # check the surrounding to see whether they are in the board or not.
    if world[row][col] == EMPTY:
        return True
    else:
        if ratio_checker(world, world_size, row, col) >= 1/3 and ratio_checker(world, world_size, row, col)!= 0:
            return True
        else:
            return False

# make a mainlist(world) where several nested list append to
    # create inside list that have with random number which
    # numbers shall be convert to EBO
# after making the world,
    # if more on one tribe, change it to emoty
    # if more
def create_world(world_size, tribe_size):
    world = []
    num_orange = 0
    num_blue = 0
    for n in range(world_size):
        list_r = []
        for n in range(world_size):
            pin = randrange(3)
            if pin == 0:
                pin = ORANGE
                num_orange += 1
            elif pin == 1:
                pin = BLUE
                num_blue += 1
            elif pin == 2:
                pin = EMPTY
            list_r.append(pin)
        world.append(list_r)
    if num_orange < tribe_size:
        for extra_emp in range(tribe_size - num_orange):
            random_index = random_spot_finder(world, world_size, EMPTY)
            world[random_index[0]][random_index[1]] = ORANGE
            num_orange += 1
    if num_blue < tribe_size:
        for extra_emp in range(tribe_size - num_blue):
            random_index = random_spot_finder(world, world_size, EMPTY)
            world[random_index[0]][random_index[1]] = BLUE
            num_blue += 1
    if num_orange > tribe_size:
        for extra_ora in range(num_orange - tribe_size):
            random_index = random_spot_finder(world, world_size, ORANGE)
            world[random_index[0]][random_index[1]] = EMPTY
            num_orange -= 1
    if num_blue > tribe_size:
        for extra_blu in range(num_blue - tribe_size):
            random_index = random_spot_finder(world, world_size, BLUE)
            world[random_index[0]][random_index[1]] = EMPTY
            num_blue -= 1
    return world


# if satisfy, return original world
# if not,
    # move this to an random empty place.
    # tag target to empty
def move(world, row, col):
    if satisfaction_check(world, len(world), row, col):
        return world
    else:
        move_spot = random_spot_finder(world, len(world), EMPTY)
        world[move_spot[0]][move_spot[1]] = world[row][col]
        world[row][col] = EMPTY
        return world

# add up the ratio of every one target
# use the function to return segregation percentage

def calculate_segregation(world):
    ratio_list = []
    total_tribe_size = 0
    for r in range(len(world)):
        for c in range(len(world)):
            ratio = ratio_checker(world, len(world), r, c)
            ratio_list.append(ratio)
            if world[r][c] != EMPTY:
                total_tribe_size += 1
    avg = (sum(ratio_list))/(total_tribe_size)
    return (avg - 0.5) / 0.5

def main():
    world_size = 40
    tribe_size = 640
    world = create_world(world_size, tribe_size)
    for timestep in range(10):
        for r in range(world_size):
            for c in range(world_size):
                world = move(world, r, c)
        print("Timestep " + str(timestep))
        print_world(world)
        print("Segregation: " + "{:.2f}".format(calculate_segregation(world)) + "%")
        print()


if __name__ == "__main__":
    main()
