#
# 기타 함수
#

def split_list(the_list: list, chunk_size: int) -> list:
    result_list = []

    while the_list:
        result_list.append(the_list[:chunk_size])
        the_list = the_list[chunk_size:]

    return result_list
