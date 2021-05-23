"""
API for converting RRRR dataset into different subsets
Lastest update: Apr. 8, 2021
"""
import os
import csv
import re
import shutil
import cv2
import argparse

class RRRRDownloader:
    def __init__(self, datapath, csvpath, outpath):
        self.datapath = datapath
        self.csvpath = csvpath
        self.outpath = outpath

    def _get_names(self, path, name):
        # helper function to get input names
        regex_str = "^%s"%(name) # start with name
        regex = re.compile(regex_str)
        inputs = os.listdir(path)
        inputs = [os.path.join(path, f) for f in inputs if regex.match(f)]

        return inputs

    def _download_helper(self, mode, folder_name):
        with open(self.csvpath,'r') as f:
            header = f.readline()
            count, total = 0, 0
            for line in f:
                row = line.strip().split(',')
                name = row[0].split('/')
                set_type = row[-1] # train/val/test

                if set_type != mode: continue

                cam_fo = name[0] # camera folder
                M = name[1] + '_M'
                R = name[1] + '_R'
                T = name[1] + '_T'
                Mimages = self._get_names(os.path.join(self.datapath,cam_fo), M)
                Rimages = self._get_names(os.path.join(self.datapath,cam_fo), R)
                Timages = self._get_names(os.path.join(self.datapath,cam_fo), T)
                total += len(Mimages)

                # move all M images to new_path
                for img in Mimages:
                    basename = os.path.basename(img)
                    new_folder = os.path.join(self.outpath, folder_name, 'M')
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                    new_name = os.path.join(new_folder, cam_fo + '_' + basename)
                    shutil.copy(img, new_name)

                # move all R images to new_path
                for img in Rimages:
                    basename = os.path.basename(img)
                    new_folder = os.path.join(self.outpath, folder_name, 'R')
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                    new_name = os.path.join(new_folder, cam_fo + '_' + basename)
                    shutil.copy(img, new_name)

                # move all T images to new_path
                for img in Timages:
                    basename = os.path.basename(img)
                    new_folder = os.path.join(self.outpath, folder_name, 'T')
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                    new_name = os.path.join(new_folder, cam_fo + '_' + basename)
                    shutil.copy(img, new_name)

                count += 1

            print("done %d images / %d crops transform"%(count, total))

    def download(self, train, val, test, type=""):
        # 0 for trainset, 1 for valset, 2 for test set
        if train:
            print("generating trainset...")
            self._download_helper('0', 'train')
        if val:
            print("generating valset...")
            self._download_helper('1', 'val')
        if test:
            print("generating testset...")
            self._download_helper('2', 'test')


def create_parser():
    parser = argparse.ArgumentParser(add_help=True)
    # paths
    parser.add_argument('--datapath', type=str, default="/home/chenyang/disk1/pami2021-raw-rr/data/pami2021/isprgb_crop/with_gt",
                        help='path to dataset')
    parser.add_argument('--csvpath', type=str, default="/home/chenyang/disk1/pami2021-raw-rr/data/pami2021/cleaned.csv",
                        help='path to csv')
    parser.add_argument('--output', type=str, default="/home/chenyang/disk1/pami2021-raw-rr/data/mydataset",
                        help='path to store the transformed dataset')
    # dataset choices
    parser.add_argument('--train', action='store_true', help='generate trainset')
    parser.add_argument('--val', action='store_true', help='generate valset')
    parser.add_argument('--test', action='store_true', help='generate testset')
    # scene choices
    parser.add_argument('--type', type=str, default="", help='BRBT/SRST/BRST')

    return parser


def parse_args(parser):
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    parser = create_parser()
    args = parse_args(parser)

    downloader = RRRRDownloader(args.datapath, args.csvpath, args.output)
    downloader.download(args.train, args.val, args.test)

    print("download done")
