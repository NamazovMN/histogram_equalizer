import os

import numpy as np
from utilities import *
from skimage.color import rgb2gray
from skimage import io
from skimage.transform import resize
from scipy import ndimage
import pickle

class ReadImages:
    def __init__(self, config_parameters: dict):
        """
        Method is utilized as an initializer for the class
        :param config_parameters: dictionary that contains all required information for the project
        """
        self.configuration = self.set_configuration(config_parameters)
        self.data = self.process()

    def set_configuration(self, parameters: dict):
        """
        Method is utilized to collect required information for the task
        :param parameters: dictionary that contains all required information for the project
        :return: dictionary that contains required information for the task
        """
        input_directory = parameters['input_dir']
        output_dir = parameters['output_dir']
        check_dir(output_dir)
        return {
            'input_dir': input_directory,
            'output_dir': output_dir,
            'dimension': (parameters['width'], parameters['height']),
            'num_pixels': parameters['width'] * parameters['height'],
            'sigma': parameters['sigma'],
            'bins': parameters['bins']
        }

    def read_resize(self, image_path: str) -> np.array:
        """
        Method is used for reading image and applying resize and gray scaling to the image
        :param image_path: path to the requested image
        :return: numpy array of an image
        """
        image = io.imread(image_path)
        image = resize(image, self.configuration['dimension'])

        return rgb2gray(image)

    def apply_gaussian(self, image_path: str) -> np.array:
        """
        Method is utilized to apply gaussian filtering
        :param image_path: path to the requested image
        :return: Gaussian filtered image
        """
        image_array = self.read_resize(image_path)
        return ndimage.gaussian_filter(image_array, sigma=self.configuration['sigma']) * 255

    def compute_histogram(self, image_array: np.array) -> tuple:
        """
        Method is utilized to compute histogram for the provided image array
        :param image_array: numpy array of an image
        :return: tuple that contains histogram bins and edges
        """
        histogram, edges = np.histogram(image_array, self.configuration['bins'])
        return histogram, edges
    
    def cumulative_sum(self, image_array: np.array) -> dict:
        """
        Method is utilized to compute cdf according to the histogram data
        :param image_array: numpy array of an image
        :return: dictionary that contains histogram and cdf information for the requested image
        """
        bins, edges = self.compute_histogram(image_array)
        cdf = np.zeros(len(bins))

        for idx, intensity in enumerate(bins):
            current = 0 if idx == 0 else cdf[idx - 1]
            cdf[idx] = current + intensity
        max_intensity = max(bins)
        max_cdf = max(cdf)
        normalized_cdf = cdf * (max_intensity / max_cdf)

        return {
            'bins': bins,
            'edges': edges,
            'cdf': cdf,
            'normalized_cdf': normalized_cdf,
            'min_cdf': min(normalized_cdf),
            'max_cdf': max(normalized_cdf),
        }

    def equalize(self, gaussian_filtered_image: np.array) -> tuple:
        """
        Method is utilized to apply equalization process
        :param gaussian_filtered_image: numpy array of gaussian filtered image
        :return: tuple which contains histogram equalized image and information dict
        """
        data_dict = self.cumulative_sum(gaussian_filtered_image)
        equalized = (data_dict['normalized_cdf'] - data_dict['min_cdf']) * 255 / \
                    (data_dict['max_cdf'] - data_dict['min_cdf']).astype('uint8')
        filtered_equalized = equalized[gaussian_filtered_image.astype('uint8')]
        equalized_image = np.reshape(filtered_equalized, gaussian_filtered_image.shape)
        return equalized_image, data_dict
    def process(self) -> dict:
        """
        Method is utilized as main function of the class, so that all required processes are applied here
        :return: information dictionary that contains all required information for the process per image
        """
        info_data = dict()
        info_file = os.path.join(self.configuration['output_dir'], 'processed_info.pickle')
        if not os.path.exists(info_file):
            for each_image in os.listdir(self.configuration['input_dir']):
                image_path = os.path.join(self.configuration['input_dir'], each_image)
                gaussian_filtered_original = self.apply_gaussian(image_path)
                image, original_data_dict = self.equalize(gaussian_filtered_original)
                equalized_data_dict = self.cumulative_sum(image)
                current_dict = {'original_info': original_data_dict, 'equalized_info': equalized_data_dict, 'image': image}
                info_data[each_image] = current_dict
            with open(info_file, 'wb') as info_save:
                pickle.dump(info_data, info_save)
        with open(info_file, 'rb') as info_save:
            info_data = pickle.load(info_save)
        return info_data

    def __getitem__(self, item: str) -> dict:
        """
        Method is a getter, so that image name is provided as an item for corresponding image process
        :param item: name of the requested image
        :return: dictionary for the corresponding image data
        """
        return self.data[item]

    def __len__(self) -> int:
        """
        Method is utilized to get length of the dataset for the process
        :return: length of dataset
        """
        return len(self.data)



