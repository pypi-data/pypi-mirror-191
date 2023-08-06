from simba.misc_tools import check_file_exist_and_readable, get_fn_ext
from simba.unsupervised.misc import check_directory_exists
from simba.rw_dfs import read_df

class ClusterVisualizer(object):
    def __init__(self,
                 video_dir: str,
                 data_path: str,
                 settings: dict):

        check_file_exist_and_readable(file_path=data_path)
        _, _, ext = get_fn_ext(data_path)
        data_df = read_df(data_path, file_type=ext[1:])
        print(data_df)





_ = ClusterVisualizer(video_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/project_folder/videos',
                      data_path='/Users/simon/Desktop/envs/troubleshooting/unsupervised/dr_models/affectionate_brahmagupta_funny_darwin.csv',
                      settings={})
