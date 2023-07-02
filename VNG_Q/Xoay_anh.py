def rotate_image_clone(image, rotation):
    m = len(image)  # m rows
    n = len(image[0])   # n columns

    if rotation == 'P' or rotation == '3T':
        rotated_image = [[image[m - j - 1][i] for j in range(m)] for i in range(n)]
    elif rotation == '2P' or rotation == '2T':
        rotated_image = [[image[m - i - 1][n - j - 1] for j in range(n)] for i in range(m)]
    elif rotation == '3P' or rotation == 'T':
        rotated_image = [[image[j][n - i - 1] for j in range(m)] for i in range(n)]

    return rotated_image

def rotate_image(image, operations):
    ds = {'P': 90, '2P': 180, '3P': 270, 'T': -90, '2T': -180, '3T': -270}
    m = len(image)  # m rows
    n = len(image[0])   # n columns

    total = 0
    for i in range(len(operations)):
        total += ds[operations[i]]


    degree = total//90
    if degree <= 0:
        degree = abs(degree)%4*-1*90+360
    else:
        degree = degree%4*90
    print (degree//90)

    match degree:
        case 1:
            rotated_image = [[image[m - j - 1][i] for j in range(m)] for i in range(n)]
        case 2:
            rotated_image = [[image[m - i - 1][n - j - 1] for j in range(n)] for i in range(m)]
        case 3:
            rotated_image = [[image[j][n - i - 1] for j in range(m)] for i in range(n)]
        case _:
            rotated_image = image

    return rotated_image


def rotated_clockwise(image):

    m = len(image)  # m rows
    n = len(image[0])   # n columns
    rotated_image = [[image[m - j - 1][i] for j in range(m)] for i in range(n)]
    return rotated_image

def rotated_image_1(image, operations):
    ds = {'P': 90, '2P': 180, '3P': 270, 'T': -90, '2T': -180, '3T': -270}
    # for row in image:
    #     print(' '.join(map(str, row)))
    total = 0
    for i in range(len(operations)):
        total += ds[operations[i]]


    degree = total//90
    if degree <= 0:
        degree = abs(degree)%4*-1*90+360
    else:
        degree = degree%4*90
    print (degree//90)

    for i in range(degree//90):
        rotated_image = rotated_clockwise(image)
        image = rotated_image

    return image

# ------- Read input file
def read_input(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

        m, n = map(int, lines[0].split())
        image = []
        for i in range(1, m+1):
            row = list(map(int, lines[i].split()))
            image.append(row)
        operations = lines[m + 1].split()
    return (image, operations)

test = read_input("demofile2.txt")
image = rotate_image(test[0], test[1])
rs = ""
for row in image:
    rs += ' '.join(map(str, row)) + "\n"
    # print(' '.join(map(str, row)))

f = open("output.txt", "w")
f.write(rs)