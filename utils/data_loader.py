def read_instance(filename):
    with open(filename, 'r') as file:

        n = int(file.readline().strip())

        coords = []
        for line in range(n):
            coords.append(list(map(float, file.readline().split())))

        dist_matrix = []
        for line in range(n):
            dist_matrix.append(list(map(float, file.readline().split())))

    return n, coords, dist_matrix