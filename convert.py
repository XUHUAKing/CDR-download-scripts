"""
API for converting CDR dataset into different subsets
Lastest update: Jun. 30, 2021
"""
import os
import csv
import re
import shutil
import argparse
import cv2

class CDRConverter:
    def __init__(self, datapath, csvpath, outpath):
        self.datapath = os.path.join(datapath, 'isprgb_crop', 'with_gt')
        self.csvpath = csvpath
        self.outpath = outpath

    def _get_names(self, path, name):
        # helper function to get input names
        regex_str = "^%s"%(name) # start with name
        regex = re.compile(regex_str)
        inputs = os.listdir(path)
        inputs = [os.path.join(path, f) for f in inputs if regex.match(f)]

        return inputs

    def _convert_helper(self, mode, folder_name, args):
        with open(self.csvpath,'r') as f:
            header = f.readline()
            total = 0
            for line in f:
                row = line.strip().split(',')
                name = row[0].split('/')
                set_type = row[-1] # train/val/test

                # skip images based on user's filters
                if set_type != mode: continue
                if args.type != 'all' and row[1] != args.type : continue
                if args.reflection != 'all' and row[2] != args.reflection : continue
                if args.ghost != 'all' and row[3] != args.ghost : continue
                if args.motion != 'all' and row[4] != args.motion : continue

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
                    os.makedirs(new_folder, exist_ok=True)
                    new_name = os.path.join(new_folder, cam_fo + '_' + basename)
                    if args.crop32 or args.downsample_scale:
                        img = cv2.imread(img, -1)
                        if args.downsample_scale:
                            # downsample
                            img = img[::args.downsample_scale, ::args.downsample_scale, :]
                        if args.crop32:
                            # crop image into 32's multiples
                            new_input_h = 32*(img.shape[0]//32)
                            new_input_w = 32*(img.shape[1]//32)
                            img = img[:new_input_h, :new_input_w, :]
                        cv2.imwrite(new_name, img)
                    else:
                        shutil.copy(img, new_name)

                # move all R images to new_path
                for img in Rimages:
                    basename = os.path.basename(img)
                    new_folder = os.path.join(self.outpath, folder_name, 'R')
                    os.makedirs(new_folder, exist_ok=True)
                    new_name = os.path.join(new_folder, cam_fo + '_' + basename)
                    if args.crop32 or args.downsample_scale:
                        img = cv2.imread(img, -1)
                        if args.downsample_scale:
                            # downsample
                            img = img[::args.downsample_scale, ::args.downsample_scale, :]
                        if args.crop32:
                            # crop image into 32's multiples
                            new_input_h = 32*(img.shape[0]//32)
                            new_input_w = 32*(img.shape[1]//32)
                            img = img[:new_input_h, :new_input_w, :]
                        cv2.imwrite(new_name, img)
                    else:
                        shutil.copy(img, new_name)

                # move all T images to new_path
                for img in Timages:
                    basename = os.path.basename(img)
                    new_folder = os.path.join(self.outpath, folder_name, 'T')
                    os.makedirs(new_folder, exist_ok=True)
                    new_name = os.path.join(new_folder, cam_fo + '_' + basename)
                    if args.crop32 or args.downsample_scale:
                        img = cv2.imread(img, -1)
                        if args.downsample_scale:
                            # downsample
                            img = img[::args.downsample_scale, ::args.downsample_scale, :]
                        if args.crop32:
                            # crop image into 32's multiples
                            new_input_h = 32*(img.shape[0]//32)
                            new_input_w = 32*(img.shape[1]//32)
                            img = img[:new_input_h, :new_input_w, :]
                        cv2.imwrite(new_name, img)
                    else:
                        shutil.copy(img, new_name)

            print("generated %d triplets"%(total))

    def convert(self, args):
        # 0 for trainset, 1 for valset, 2 for test set
        if args.train:
            print("generating trainset...")
            self._convert_helper('0', 'train', args)
        if args.val:
            print("generating valset...")
            self._convert_helper('1', 'val', args)
        if args.test:
            print("generating testset...")
            self._convert_helper('2', 'test', args)


def create_parser():
    parser = argparse.ArgumentParser(add_help=True)
    # paths
    parser.add_argument('--datapath', type=str, required=True,
                        help='path to dataset')
    parser.add_argument('--csvpath', type=str, required=True,
                        help='path to csv')
    parser.add_argument('--output', type=str, required=True,
                        help='path to store the converted (sub) dataset')
    # dataset choices
    parser.add_argument('--train', action='store_true', help='generate trainset')
    parser.add_argument('--val', action='store_true', help='generate valset')
    parser.add_argument('--test', action='store_true', help='generate testset')
    parser.add_argument('--crop32', action='store_true', help='some methods require image size of a multiple of 32, this option help crop the image')
    parser.add_argument('--downsample_scale', type=int, help='downsample x N, N must be integer')
    # scene choices
    parser.add_argument('--type', type=str, default="all", choices=['BRBT', 'SRST', 'BRST', 'all'], help='scene type')
    parser.add_argument('--reflection', type=str, default="all", choices=['strong', 'medium', 'weak', 'all'], help='reflection type')
    parser.add_argument('--ghost', type=str, default="all", choices=['0', '1', 'all'], help='generate subset with ghost effect')
    parser.add_argument('--motion', type=str, default="all", choices=['0', '1', 'all'], help='generate subset with motion blur')

    return parser


def parse_args(parser):
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    parser = create_parser()
    args = parse_args(parser)

    downloader = CDRConverter(args.datapath, args.csvpath, args.output)
    downloader.convert(args)

    print("Done! Your subset(s) are ready!")
