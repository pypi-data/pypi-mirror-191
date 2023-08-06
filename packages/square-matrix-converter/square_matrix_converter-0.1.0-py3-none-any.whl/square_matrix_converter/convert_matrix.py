def convert_matrix(matrix: str) -> list[list[int]] | ValueError:
    """
    The function converts the representation of a string matrix
    to a square matrix.
    """
    if matrix:
        rows = matrix.strip().split("\n")[1::2]
        square_matrix = []

        for row in rows:
            row = row.replace("|", " ").split()
            if row:
                square_matrix.append(list(map(int, row)))

        if square_matrix:
            return square_matrix

    raise ValueError(
        "Unfortunately, the string matrix representation is empty."
    )
