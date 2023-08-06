def convert_square_matrix(
    square_matrix: list[list[int]],
) -> list[int] | ValueError:
    """
    The function converts the square matrix to the one-dimensional list.
    The transformation starts from the lower right corner and
    continues in a clockwise direction.
    """
    one_dimensional_list = []
    left, right = 0, len(square_matrix) - 1
    top, bottom = 0, len(square_matrix[0]) - 1

    if right == bottom:
        while left <= right and top <= bottom:
            for column in range(right, left - 1, -1):
                one_dimensional_list.append(square_matrix[bottom][column])

            bottom -= 1

            for row in range(bottom, top - 1, -1):
                one_dimensional_list.append(square_matrix[row][left])

            left += 1

            for column in range(left, right + 1):
                one_dimensional_list.append(square_matrix[top][column])

            top += 1

            for row in range(top, bottom + 1):
                one_dimensional_list.append(square_matrix[row][right])

            right -= 1

        return one_dimensional_list

    raise ValueError("Unfortunately, this is not a square matrix.")
