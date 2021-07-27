# CDR Converter
We provide the python script to convert the dataset proposed in _CDR: A Categorized and Diverse Real-World Reflection Removal Dataset_ based on different options.

## Setup
The script requires Python 3.5+ and cv2.
Please download our data (~7.45GB) from this [link](https://hkustconnect-my.sharepoint.com/:f:/g/personal/xhuangat_connect_ust_hk/EkjThMWOhT1EoKrK-U6l8EkB9BeKQjPNjB3mlK2omAZQIw?e=YPb48i). We have 1063 triplets (M, R, T) in total.

## Usage
```
python convert.py --datapath <DATAPATH> --csvpath <CSVPATH> --output <OUTPUTDIR> --[options]
```

You can choose to generate one (or a subset) of our dataset by setting the following self-explanatory arguments:

- ```--train```
- ```--val```
- ```--test```
- ```--type```
- ```--reflection```
- ```--ghost```
- ```--motion```

For example, if you want to down only train set,
```
python convert.py --datapath <DATAPATH> --csvpath <CSVPATH> --output <OUTPUTDIR> --train
```

Note that these arguments can be combined to generate a set satisfying all options,

```
python convert.py --datapath <DATAPATH> --csvpath <CSVPATH> --output <OUTPUTDIR> --test --type SRST --reflection medium
```

will generate testset with SRST type AND medium reflection.

Considering some methods may require input image in size of a multiple 32, we also provide an argument ```--crop32```, which will generate images in size of its nearest 32's multiples.

Some crops in our dataset may have large ratio of longer side / shorter side, you can remove those crops by ```--remove_extreme```

Our dataset is in high resolution, so we also support downsampling option by specifying ```--downsample_scale``` argument followed by an integer.
## Output
You must specify the output folder with ```--output``` argument.

### Folders structure
You should expect the original data structure looks like
```
data/
└── isprgb_crop
    └── with_gt
        ├── C1
        ├── C10
        ├── C11
        ├── C2
        ├── C3
        ├── C4
        ├── C5
        ├── C6
        ├── C7
        ├── C8
        ├── C9
        ├── H1
        ├── N1
        ├── N2
        ├── N3
        ├── N4
        ├── N5
        ├── N6
        └── N7
```
- **isprgb_crop**: cropped data inside valid regions

Each leaf directory will contain ```.png``` files accordingly. Also, there is a four unique digit number (e.g. 5532, 5531) for each M and R image, while the corresponding T image is named as "M_R" (e.g. 5532_5531).

For normal benchmarking (as written in our script), only **isprgb_crop/** folder will be used, so we only make this folder public for the first release. 
<!-- However, you are also welcome to play with the original data. But please ensure that only valid region bounded by mask are valid for _T = M-R_. -->

## Citation
If you find this dataset or code useful, please kindly reference:
```

```
