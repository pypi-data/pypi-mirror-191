import aiohttp

from square_matrix_converter.convert_matrix import convert_matrix
from square_matrix_converter.convert_square_matrix import convert_square_matrix


async def parse_matrix(url: str) -> list[int] | Exception:
    """
    The function retrieve a matrix from a specified URL and return one-dimensional list.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                status_code = response.status
                if 400 <= status_code < 500:
                    raise Exception(
                        f"Unfortunately, an error occurred on the client side, "
                        f"status code: {status_code}."
                    )
                elif status_code >= 500:
                    raise Exception(
                        f"Unfortunately, a server-side error occurred, "
                        f"status code: {status_code}"
                    )
                matrix = await response.text()
                square_matrix = convert_matrix(matrix)
                one_dimensional_list = convert_square_matrix(square_matrix)

                return one_dimensional_list
    except (aiohttp.ClientError, aiohttp.ClientTimeout) as client_error:
        raise Exception(
            f"Unfortunately, there was a connection error: {client_error}."
        )
    except TimeoutError as timeout_error:
        raise Exception(
            f"Unfortunately, timeout error occurred: {timeout_error}."
        )
    except ConnectionRefusedError as connection_error:
        raise Exception(
            f"Unfortunately, connection refused: {connection_error}."
        )
