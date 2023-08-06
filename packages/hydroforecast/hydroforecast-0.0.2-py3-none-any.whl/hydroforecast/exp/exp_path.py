import os


class ExpPath(object):
    def __init__(self, proj_path, proj_nm, model_nm, seed):
        self.checkpoint_path = os.path.join(proj_path, 'checkpoint', proj_nm, model_nm, 'seed_{}'.format(seed))
        self.save_path = os.path.join(proj_path, 'save', proj_nm, model_nm, 'seed_{}'.format(seed))
        self.log_path = os.path.join(proj_path, 'log', proj_nm, model_nm, 'seed_{}'.format(seed))
        self.db_save_path = os.path.join(proj_path, 'db_save', proj_nm, model_nm)
        self.tune_path = os.path.join(self.checkpoint_path, 'tune_result')
        self.make_dirs()

    def make_dirs(self):
        for path in [self.checkpoint_path, self.save_path, self.tune_path, self.log_path, self.db_save_path]:
            if not os.path.exists(path):
                os.makedirs(path)

    def clear_dirs(self):
        # todo 用于删除文件夹方便重新训练
        pass
