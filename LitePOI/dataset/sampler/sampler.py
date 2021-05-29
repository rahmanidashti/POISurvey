
__version__ = '0.1'
__author__ = 'Hossein A. Rahmani'
__email__ = 'rahmanidashti@alumni.znu.ac.ir'

from collections import defaultdict
import random
random.seed(9999)
import math
import os
import argparse


def parse_args():
    # Define the program description and its usage
    text = 'This is a sampler program.'

    # Initiate the parser
    parser = argparse.ArgumentParser(description=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-d", "--dataset", type=str, default='gowalla', help="select dataset")
    parser.add_argument("-t", "--type", type=str, default='min', help="select type of dataset (full or min)")
    parser.add_argument("-r", "--rate", type=list, nargs="+", default=[20, 40, 60, 80], help="add sample rates")
    parser.add_argument("-v", "--version", default='0.1', help="version of sampler program", action="store_true")

    args = parser.parse_args()

    return args


def path_to_save(sample_file, sample_rate):
    """
    Method creates a folder based on the dataset name and sample rate to add the output files

    Parameters
    ----------
    sample_file: str, the name of file
    sample_rate: str, the rate of sampling

    Returns
    -------
    dataset_name: str, the name of dataset
    sample_name: str, the name of sample
    sample_root: str, the path of sample
    """

    dataset_name = sample_file.split('/')[4].split('_')[0]
    sample_name = sample_file.split('/')[4].split('_')[1].split('.')[0]
    sample_root = 'data_samples/' + dataset_name + '_' + sample_name + '/' + str(sample_rate)

    if not os.path.exists(sample_root):
        os.mkdir(sample_root)
        print("Directory ", sample_root, " created.")
    else:
        print("Directory ", sample_root, " already exists.")

    return dataset_name, sample_name, sample_root


def uniform_sampling_unique_checkins(sample_file, sample_rate):
    random.seed(99)
    dataset_name, sample_name, sample_root = path_to_save(sample_file, sample_rate)

    sample_data = open(sample_file, 'r').readlines()
    users_visits = defaultdict(list)
    all_users = set()
    for eachline in sample_data:
        uid, lid, freq = eachline.strip().split()
        uid, lid, freq = int(uid), int(lid), int(freq)
        all_users.add(uid)
        users_visits[uid].append([lid, freq])

    new_sample_file = open(sample_root + '/' + dataset_name + '_' + sample_name + ".txt", 'w')

    for uid in all_users:
        user_visits = users_visits[uid]
        considered_visit_count = math.ceil((len(user_visits) * sample_rate) / 100)
        random_visits = random.sample(range(0, len(user_visits)), k=considered_visit_count)
        for random_visit in random_visits:
            lid, freq = user_visits[random_visit][0], user_visits[random_visit][1]
            new_sample_file.write(str(uid) + '\t' + str(lid) + '\t' + str(freq) + '\n')


def uniform_sampling_all_checkins(sample_file, sample_rate):

    dataset_name, sample_name, sample_root = path_to_save(sample_file, sample_rate)

    sample_data = open(sample_file, 'r').readlines()
    users_visits = defaultdict(list)
    all_users = set()
    for eachline in sample_data:
        uid, lid, freq = eachline.strip().split()
        uid, lid, freq = int(uid), int(lid), int(freq)
        all_users.add(uid)
        for count in range(freq):
            users_visits[uid].append(lid)

    new_sample_file = open(sample_root + '/' + dataset_name + '_' + sample_name + ".txt", 'w')

    selected_visits_freq = dict()
    for uid in all_users:
        user_visits = users_visits[uid]
        considered_visit_count = math.ceil((len(user_visits) * sample_rate) / 100)
        random_visits = random.sample(range(0, len(user_visits)), k=considered_visit_count)

        for random_visit in random_visits:
            lid = user_visits[random_visit]
            if lid in selected_visits_freq.keys():
                selected_visits_freq[lid] += 1
            else:
                selected_visits_freq[lid] = 1

        for lid, freq in selected_visits_freq.items():
            new_sample_file.write(str(uid) + '\t' + str(lid) + '\t' + str(freq) + '\n')

        selected_visits_freq.clear()


if __name__ == '__main__':

    args = parse_args()

    data_path = "../../../data/"
    data_dir = data_path + args.dataset + "_" + args.type + "/"
    train_file = data_dir + args.dataset + "_train.txt"

    sample_files = [train_file]
    sample_rates = args.rate

    for sample_file in sample_files:
        for sampe_rate in sample_rates:
            uniform_sampling_all_checkins(sample_file=sample_file, sample_rate=sampe_rate)
