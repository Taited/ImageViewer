import os
import os.path as osp


def get_file_names(path: str):
    file_list = []
    for file_name in os.listdir(path):
        if file_name[0] == '.':
            continue
        file_list.append(file_name)
    file_list.sort()
    return file_list

def concat_page_data(project_name, category_list: list, 
                     id_begin: int = 1, fetch_num: int = 10,
                     api_path: str = '/image_bed'):
    assert id_begin >= 1, "The begin id could not less than 1 but get: {}".format(id_begin)
    page_data = []
    for id_name in range(id_begin, id_begin + fetch_num):
        row_data = []
        for category_name in category_list:
            row_data.append(
                osp.join(api_path, project_name, 
                         category_name, '{}.png'.format(id_name)))
        page_data.append((id_name, row_data))
    return page_data
