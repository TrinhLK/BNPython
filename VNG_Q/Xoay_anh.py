def rotate_image(image, rotation):
    rows = len(image)
    cols = len(image[0])

    if rotation == 'P' or rotation == '3T':
        rotated_image = [[image[rows - j - 1][i] for j in range(rows)] for i in range(cols)]
    elif rotation == '2P' or rotation == '2T':
        rotated_image = [[image[rows - i - 1][cols - j - 1] for j in range(cols)] for i in range(rows)]
    elif rotation == '3P' or rotation == 'T':
        rotated_image = [[image[j][cols - i - 1] for j in range(rows)] for i in range(cols)]
    # elif rotation == 'T':
    #     rotated_image = [[image[j][cols - i - 1] for j in range(rows)] for i in range(cols)]
    # elif rotation == '2T':
    #     rotated_image = [[image[rows - i - 1][cols - j - 1] for j in range(cols)] for i in range(rows)]
    # elif rotation == '3T':
    #     rotated_image = [[image[rows - j - 1][i] for j in range(rows)] for i in range(cols)]

    return rotated_image


def main():
    # filename = input("Nhập tên file đầu vào: ")

    with open("Inp_xoayanh.txt", 'r') as file:
        lines = file.readlines()

        m, n = map(int, lines[0].split())
        image = []
        for i in range(1, m+1):
            row = list(map(int, lines[i].split()))
            image.append(row)
            print (row)

        # num_operations = int(lines[m])
        operations = lines[m + 1].split()

        for op in operations:
            image = rotate_image(image, op)

        for row in image:
            print(' '.join(map(str, row)))


if __name__ == "__main__":
    main()