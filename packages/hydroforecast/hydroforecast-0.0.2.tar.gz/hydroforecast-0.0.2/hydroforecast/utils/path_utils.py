import os
import numpy as np


def get_pl_model_states_path(exp_path, model_id):
    best_trial_path = os.path.join(exp_path.checkpoint_path, 'tune_history', 'trial_{}'.format(model_id),
                                   'lightning_logs')
    recent_log = os.listdir(best_trial_path)[-1]
    best_trial_path = os.path.join(best_trial_path, recent_log, 'checkpoints')

    model_states_name = os.listdir(best_trial_path)
    best_states = np.argmin(np.array([float(nm.split('-')[1].split('=')[1].split('.ckpt')[0]) for nm in model_states_name]))

    return os.path.join(best_trial_path, model_states_name[best_states])


def get_pl_model_states_path_v2(exp_path, model_id):
    # without log
    best_trial_path = os.path.join(exp_path.checkpoint_path, 'tune_history', 'trial_{}'.format(model_id))
    best_trial_path = os.path.join(best_trial_path, 'checkpoints')
    model_states_name = os.listdir(best_trial_path)
    best_states = np.argmin(np.array([float(nm.split('-')[1].split('=')[1].split('.ckpt')[0]) for nm in model_states_name]))

    return os.path.join(best_trial_path, model_states_name[best_states])
