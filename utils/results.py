from pulp import value

def get_tour_string(n, x):
    tour = [0]
    current = 0
    while len(tour) < n:
        for j in range(n):
            if j != current and value(x[current, j]) > 0.5:
                tour.append(j)
                current = j
                break

    # Add start to end to close loop and format to 1-based index
    return " -> ".join(str(city + 1) for city in tour + [0])