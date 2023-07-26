import os
import os.path as osp


DIR = '/mnt/tedsun/cafidata/SSDiff_vis'

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
                     api_path: str = '/image/image_bed'):
    assert id_begin >= 1, "The begin id could not less than 1 but get: {}".format(id_begin)
    page_data = []
    for id_name in range(id_begin, id_begin + fetch_num):
        row_data = []
        for category_name in category_list:
            if category_name == 'text_info' or category_name == 'txt':
                txt_flag = True
                data_api = osp.join(DIR, project_name, 
                                    category_name, '{}.txt'.format(id_name))
                with open(data_api, 'r') as fp:
                    data_api = fp.read()
                    fp.close()
            else:
                txt_flag = False
                data_api = osp.join(api_path, project_name, 
                                    category_name, '{}.png'.format(id_name))
            row_data.append((txt_flag, data_api))
        page_data.append((id_name, row_data))
    return page_data
