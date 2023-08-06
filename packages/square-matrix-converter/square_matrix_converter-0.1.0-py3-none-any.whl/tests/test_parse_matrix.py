import asyncio

from square_matrix_converter import parse_matrix


SOURCE_URL = "https://raw.githubusercontent.com/koury/pymx/main/source.txt"
EXPECTED = [
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
]


def test_parse_matrix() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    one_dimensional_list = loop.run_until_complete(parse_matrix(SOURCE_URL))
    assert one_dimensional_list == EXPECTED
