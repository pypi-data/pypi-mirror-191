import pytest

from square_matrix_converter import convert_square_matrix


@pytest.mark.parametrize(
    "square_matrix,one_dimensional_list",
    [
        (
            [[10]],
            [10],
        ),
        (
            [[10, 20]],
            ValueError,
        ),
        (
            [[10, 20], [30, 40]],
            [40, 30, 10, 20],
        ),
        (
            [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
            [90, 80, 70, 40, 10, 20, 30, 60, 50],
        ),
        (
            [[10, 20, 30], [40, 50, 60]],
            ValueError,
        ),
        (
            [
                [10, 20, 30, 40],
                [50, 60, 70, 80],
                [90, 100, 110, 120],
                [130, 140, 150, 160],
            ],
            [
                160,
                150,
                140,
                130,
                90,
                50,
                10,
                20,
                30,
                40,
                80,
                120,
                110,
                100,
                60,
                70,
            ],
        ),
        (
            [
                [10, 20, 30, 40, 50],
                [60, 70, 80, 90, 100],
                [110, 120, 130, 140, 150],
                [160, 170, 180, 190, 200],
                [210, 220, 230, 240, 250],
            ],
            [
                250,
                240,
                230,
                220,
                210,
                160,
                110,
                60,
                10,
                20,
                30,
                40,
                50,
                100,
                150,
                200,
                190,
                180,
                170,
                120,
                70,
                80,
                90,
                140,
                130,
            ],
        ),
    ],
)
def test_convert_square_matrix(
    square_matrix: list[list[int]],
    one_dimensional_list: list[int] | ValueError,
) -> None:
    if isinstance(one_dimensional_list, list):
        assert convert_square_matrix(square_matrix) == one_dimensional_list
    else:
        with pytest.raises(
            ValueError, match="Unfortunately, this is not a square matrix."
        ):
            convert_square_matrix(square_matrix)
