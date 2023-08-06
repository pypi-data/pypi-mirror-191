import cv2
import numpy as np
import os
import fiiireflyyy.firefiles as ff

from imaris_ims_file_reader.ims import ims
import zarr
from PIL import Image


def scale_range(value, min_measurement, max_measurement, min_target=0,
                max_target=255):
    """
    scale measurement value given an interval.

        Parameters
        ----------
        value : int, float
            The value to scale
        min_measurement : int, float
            The minimal measured value of the sample to scale.
        max_measurement : int, float
            The maximal measured value of the sample to scale.
        min_target : int, float, optional, default : 0
            The lower limit of the interval used for scaling.
        max_target : int, float, optional, default : 255
            The upper limit of the interval used for scaling.

        Returns
        -------
        out : int, float
            The scaled value
    """
    scaled_value = (value - min_measurement) / (max_measurement - min_measurement) * (
            max_target - min_target) + min_target
    return scaled_value


def combine(images, z_mode='firstlayer'):
    """
    combine multiple images of the same size as one.

        Parameters
        ----------
        images : list of PIL Image instances

        z_mode : {'firstlayer', 'midlayer', 'endlayer', 'max', 'average'}, optional, default : 'firstlayer'
            How to process the z dimension of the ims file.
            'firstlayer', 'midlayer' and 'endlayer' will process only the first, middle or last z layer respectively.
            'max' takes account of all z layers. Per channel and per pixel, select the highest value among all the z.
            'average' takes account of all z layers. Per channel and per pixel, make the average among all the z.

        Returns
        -------
        out : a Pillow Image instance

    """
    h, w = images[0].size
    merged_array = np.zeros((h, w, 3), dtype=np.uint8)
    converted_image = Image.fromarray(merged_array, 'RGB')

    if z_mode == 'midlayer':
        mid_idx = int(len(images) / 2)
        converted_image = images[mid_idx]

    elif z_mode == 'firstlayer':
        converted_image = images[0]

    elif z_mode == 'endlayer':
        converted_image = images[len(images)]

    elif z_mode == 'max':
        for img_idx in range(len(images)):
            img = images[img_idx]
            # noinspection PyTypeChecker
            img_matrix = np.asarray(img)
            for y in range(h):
                for x in range(w):
                    r, g, b = img_matrix[x, y]
                    new_r = max(merged_array[x, y][0], r)
                    new_g = max(merged_array[x, y][1], g)
                    new_b = max(merged_array[x, y][2], b)
                    merged_array[x, y] = [new_r, new_g, new_b]
        converted_image = Image.fromarray(merged_array, 'RGB')

    elif z_mode == 'average':
        for y in range(h):
            for x in range(w):
                r_values = []
                g_values = []
                b_values = []
                for img_idx in range(len(images)):
                    # noinspection PyTypeChecker
                    img_matrix = np.asarray(images[img_idx])
                    r, g, b = img_matrix[x, y]
                    r_values.append(r)
                    g_values.append(g)
                    b_values.append(b)
                merged_array[x, y] = [int(np.mean(r_values)), int(np.mean(g_values)), int(np.mean(b_values))]
        converted_image = Image.fromarray(merged_array, 'RGB')

    return converted_image


def ims_to_png(ims_path, **kwargs):
    """
    convert an .ims file picture (Imaris) into a .png file.

        Parameters
        ----------
        ims_path : str
            complete path where the file to convert is stored
        
        **kwargs: keywords arguments
            mode : str, optional, default : 'RGB'
                made of the combination of 'R' 'G' and 'B' corresponding to the red green and blue channels of the
                image respectively. Any channel present will be processed in the resulting png file. The channels
                not represented will have pixels values at 0.
    
            z_mode : {'firstlayer', 'midlayer', 'endlayer', 'max', 'average'}, optional, default : 'firstlayer'
                How to process the z dimension of the ims file.
                'firstlayer', 'midlayer' and 'endlayer' will process only the first, middle or last z layer respectively.
                'max' takes account of all z layers. Per channel and per pixel, select the highest value among all the z.
                'average' takes account of all z layers. Per channel and per pixel, make the average among all the z.
    
            minmax_scaling : {'auto', } or tuple of ints, optional, default : 'auto'
                Used to scale the intensity values in the ims file between target values 0 and 255.
                if 'auto' takes the minimum and maximum measurement values as the min and max intensity in each channel.
                if (int, int), the first value is the min measurement value and the second is the max.
    
            save : str, optional, default : ''
                path where the resulting image is saved as a png.
    
            show : bool, optional, default : False
                if True, display the resulting png image in a window.

        Returns
        -------
        out : a Pillow Image
    """
    options = {"mode": 'RGB', "z_mode": "firstlayer", "minmax_scaling": 'auto', "show": False,
               "save": ""}
    options.update(**kwargs)
    # Get the channels to process
    channels_state = {'R': 0, 'G': 1, 'B': 2}

    store = ims(ims_path, ResolutionLevelLock=2, aszarr=True)
    zarray = zarr.open(store, mode='r')
    w = zarray.shape[-2]
    h = zarray.shape[-1]
    max_depth = 1
    if options["z_mode"] not in ("firstlayer", "midlayer", 'endlayer'):
        max_depth = zarray.shape[-3]

    # ------------- SELECTING THE CHANNELS TO PROCESS --------------------
    channels_to_process = []
    for channel in channels_state:
        if channel in options["mode"]:
            channels_to_process.append(channel)

    all_depths_pictures = []
    for z in range(max_depth):  # parsing all depths
        fused_data = np.zeros((h, w, 3), dtype=np.uint8)
        for channel in channels_to_process:  # processing all color channels

            # --------------------------- SCALING PREPARATION ---------------------------------
            min_intensity = 0
            max_intensity = 0

            single_channel_picture = zarray[0, channels_state[channel], z]

            if isinstance(options["minmax_scaling"], str):
                if options["minmax_scaling"] == 'auto':
                    min_intensity = single_channel_picture[0][0]
                    max_intensity = single_channel_picture[0][0]
                    for x in range(w):
                        for y in range(h):
                            if single_channel_picture[x][y] > max_intensity:
                                max_intensity = single_channel_picture[x][y]
                            if single_channel_picture[x][y] < min_intensity:
                                min_intensity = single_channel_picture[x][y]

            elif isinstance(options["minmax_scaling"], type((0, 0))):
                min_intensity = options["minmax_scaling"][0]
                max_intensity = options["minmax_scaling"][1]

            # ------------------------- RECONSTRUCTING THE IMAGE ------------------------
            for y in range(h):
                for x in range(w):
                    value = single_channel_picture[x][y]
                    scaled_value = scale_range(value, min_intensity, max_intensity)

                    if channel == 'R':
                        fused_data[x][y] = [scaled_value, fused_data[x][y][1], fused_data[x][y][2]]
                    if channel == 'G':
                        fused_data[x][y] = [fused_data[x][y][0], scaled_value, fused_data[x][y][2]]
                    if channel == 'B':
                        fused_data[x][y] = [fused_data[x][y][0], fused_data[x][y][1], scaled_value]
        img = Image.fromarray(fused_data, 'RGB')
        all_depths_pictures.append(img)

    converted_image = combine(all_depths_pictures, z_mode=options["z_mode"])
    if options["show"]:
        converted_image.show()
    if options["save"]:
        converted_image.save(options["save"])
    return converted_image


def show_image(title, image):
    """
    Show an image and wait for interaction before closing

        Parameters
        ----------
        title: str
            Title of the picture's windows.
        image: cv2 object
            The picture to show.
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)


def rotate_image(image, angle):
    """
    Rotate a picture

        Parameters
        ----------
        image: cv2 Object
            The picture to rotate
        angle: float
            Rotation angle

        Returns
        -------
        out: cv2 Object
            Rotated picture
    """
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def flip_image(image, orientation):
    """
    Flip a picture

        Parameters
        ----------
        image: cv2 Object
            The picture to flip
        orientation: {'x', 'y', 'xy'}
            The axis upon which to flip the picture. Take values "x", "y", "xy".

        Returns
        -------
        out: cv2 object
            the flipped image
        """
    if orientation.lower() == "x":
        flip = cv2.flip(image, 0)
        return flip
    elif orientation.lower() == "y":
        flip = cv2.flip(image, 1)
        return flip
    elif orientation.lower() == "xy":
        flip = cv2.flip(image, -1)
        return flip


def save_image(path, image):
    """
    Save an image on the system.

        Parameters
        ----------
        path: str
            Where to save the picture
        image: cv2 object
            The picture to save.

    """
    head, tail = os.path.split(path)
    isExist = os.path.exists(head)
    if isExist:
        cv2.imwrite(path, image)
    else:
        os.mkdir(head)
        cv2.imwrite(path, image)


def slice_images(source, destination, slice_size):
    """
    Slice all images in the source directory in multiple square sized images and save them in destination. The image
    must be square sized.

        Parameters
        ----------
        source: str
            directory where all images to slice are.
        destination: str
            where the sliced images will be saved.
        slice_size: int
            the square size of the sliced image.
    """

    images_paths = ff.get_all_files(source)
    img = cv2.imread(images_paths[0])
    img_size = img.shape[1]

    if img.shape[0] != img.shape[1]:
        raise ValueError(f"The image is not square sized: width:{img.shape[1]} != height:{img.shape[0]}")
    if img_size < slice_size:
        raise ValueError(f"Slicing size superior to image size: {slice_size} > {img_size}")

    for path in images_paths:
        slice_number = 1
        for x in range(0, img_size, slice_size):
            x1 = x
            x2 = x + slice_size

            for y in range(0, img_size, slice_size):
                y1 = y
                y2 = y + slice_size

                img = cv2.imread(path)
                sliced_img = img[y1:y2, x1:x2]

                title = destination + os.path.basename(path).split(".")[0] + "_sliced_" + str(slice_number) + ".png"

                ff.verify_dir(destination)

                cv2.imwrite(title, sliced_img)

                slice_number += 1
