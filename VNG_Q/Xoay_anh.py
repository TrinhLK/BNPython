def rotate_image(image, rotation):
    m = len(image)  # m rows
    n = len(image[0])   # n columns

    if rotation == 'P' or rotation == '3T':
        rotated_image = [[image[m - j - 1][i] for j in range(m)] for i in range(n)]
    elif rotation == '2P' or rotation == '2T':
        rotated_image = [[image[m - i - 1][n - j - 1] for j in range(n)] for i in range(m)]
    elif rotation == '3P' or rotation == 'T':
        rotated_image = [[image[j][n - i - 1] for j in range(m)] for i in range(n)]

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