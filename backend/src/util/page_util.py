def get_offset(page: int, size: int):
    if page is None:
        page = 1

    if size is None:
        size = 100

    return (page - 1) * size
