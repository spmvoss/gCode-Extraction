import math

def intermediates(p1, p2, d2 = 0.1**2):
    """"Return a list of nb_points equally spaced points
    between p1 and p2"""
    # If we have 8 intermediate points, we have 8+1=9 spaces
    # between p1 and p2

    # dis2 = x_spacing^2 + y_spacing ^2
    #
    # x2 = (p2[0] - p1[0])^2 / (n^2 + 2*n + 1)
    # y2 = (p2[1] - p1[1])^2/ (n^2 + 2*n + 1)
    #
    # d2 = (p2[0] - p1[0])^2 / (n^2 + 2*n + 1) + (p2[1] - p1[1])^2/ (n^2 + 2*n + 1)
    # d2 = ((p2[0] - p1[0])^2  + (p2[1] - p1[1])^2) / (n^2 + 2*n + 1)
    # (n^2 + 2*n + 1) = ((p2[0] - p1[0])^2  + (p2[1] - p1[1])^2) / d2
    # ((p2[0] - p1[0]) ^ 2 + (p2[1] - p1[1]) ^ 2) / d2 = c
    # n^2 +2*n + 1-c = 0
    c = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) / d2
    D = 2**2 - (4 * (1-c))  # discriminant

    if D < 0:
        print('No Solution')
    elif D == 0:
        n = -2 / (2 * 1)
        n = int(n)
    else:  # if D > 0
        n = (-2 + math.sqrt(D)) / (2 * 1)
        n = int(n)
        # x2 = (-2 - math.sqrt(D)) / (2 * 1)
        if n < 1:
            print("Initial Points Too Close Together")
        else:
            print(n)


    x_spacing = (p2[0] - p1[0]) / (n + 1)
    y_spacing = (p2[1] - p1[1]) / (n + 1)

    return [[p1[0] + i * x_spacing, p1[1] +  i * y_spacing]
            for i in range(1, n+1)]

p1 = [0, 0]
p2 = [0, 0.5]
print(intermediates(p1,p2,d2=0.2**2))