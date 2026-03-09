def distance(lst1,lst2):
    if len(lst1) != len(lst2):
        raise ValueError("Strings must be of the same length")
    distance = 0
    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            distance += 1
    return distance