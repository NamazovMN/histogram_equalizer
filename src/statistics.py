import numpy as np

from utilities import *
import random
import matplotlib.pyplot as plt
from src.image_read import ReadImages


class Statistics:
    """
    Class is used for generation of statistics
    """

    def __init__(self, config_parameters: dict, reader: ReadImages):
        """
        Method is utilized as an initializer for the class
        :param config_parameters: dictionary that contains all required information for the project
        :param reader: ReadImages object to read and process images
        """
        self.configuration = self.set_configuration(config_parameters, reader)

    @staticmethod
    def set_configuration(parameters: dict, reader: ReadImages) -> dict:
        """
        Method is utilized to collect required information for the task
        :param parameters: dictionary that contains all required information for the project
        :param reader: ReadImages object to read and process images
        :return: dictionary that contains required information for the task
        """
        check_dir('examples_dir')
        return {
            'input_dir': parameters['input_dir'],
            'examples_dir': 'examples_dir',
            'reader': reader
        }

    def get_random(self) -> tuple:
        """
        Method is used to select random image from the dataset
        :return: path to the folder in which statistics of randomly selected image will be saved and path to the image
        """
        chosen_image_path = random.choice(list(self.configuration['reader'].data.keys()))
        return os.path.join(self.configuration['examples_dir'], chosen_image_path), chosen_image_path

    @staticmethod
    def plot_comparison(original: np.array, modified: np.array, info: dict = None,
                        histogram: bool = False) -> None:
        """
        Method is utilized to plot two images for comparison purpose
        :param original: Original image before modification was applied
        :param modified: Image with applied modification
        :param info: dictionary that contains image information for figure
        :param histogram: boolean variable specifies whether comparison is done for images or histograms
        :return: None
        """
        figure, images = plt.subplots(1, 2)
        images[0].hist(original) if histogram else images[0].imshow(original, cmap="gray")
        images[0].title.set_text(info['before'])
        images[1].hist(modified) if histogram else images[1].imshow(modified, cmap="gray")
        images[1].title.set_text(info['after'])
        figure.suptitle(info['title'])
        figure.savefig(info['path'])

    def compare_gaussian(self, chosen_path: str, result_dir: str) -> None:
        """
        Method is utilized to compare original image and Gaussian applied image
        :param chosen_path: randomly selected image path (image name)
        :param result_dir: directory for statistics of the selected image
        :return: None
        """
        image_path = os.path.join(self.configuration['input_dir'], chosen_path)

        gaussian_image = self.configuration['reader'].apply_gaussian(image_path)
        original_image = self.configuration['reader'].read_resize(image_path)
        image_info = {
            'before': 'Original gray scale',
            'after': 'Gaussian filtered',
            'title': 'Gaussian filter results',
            'path': os.path.join(result_dir, 'gaussian.png')
        }
        self.plot_comparison(original_image, gaussian_image,
                             image_info)

    def compare_equalized(self, chosen_path: str, result_dir: str) -> None:
        """
        Method is utilized to compare original image and histogram equalization applied image
        :param chosen_path: randomly selected image path (image name)
        :param result_dir: directory for statistics of the selected image
        :return: None
        """
        image_path = os.path.join(self.configuration['input_dir'], chosen_path)
        equalized_image = self.configuration['reader'][chosen_path]['image']
        original_image = self.configuration['reader'].read_resize(image_path)
        image_info = {
            'before': 'Original gray scale',
            'after': 'Histogram equalized',
            'title': 'Equalization results',
            'path': os.path.join(result_dir, 'equalized.png')
        }
        self.plot_comparison(original_image, equalized_image,
                             image_info)

    def compare_histograms(self, chosen_path: str, result_dir: str) -> None:
        """
        Method is utilized to compare original histogram and equalized histogram plots
        :param chosen_path: randomly selected image path (image name)
        :param result_dir: directory for statistics of the selected image
        :return: None
        """
        original_histogram = self.configuration['reader'][chosen_path]['image']
        equalized_histogram = self.configuration['reader'][chosen_path]['image']
        image_info = {
            'before': 'Original histogram',
            'after': 'Equalized histogram',
            'title': 'Equalization results in terms of histograms',
            'path': os.path.join(result_dir, 'histograms.png')
        }
        self.plot_comparison(original_histogram, equalized_histogram,
                             image_info, histogram=True)

    def show_statistics(self) -> None:
        """
        Method is utilized for providing all required statistics
        :return: None
        """
        result_dir, chosen_image = self.get_random()
        check_dir(result_dir)
        self.compare_gaussian(chosen_image, result_dir)
        self.compare_equalized(chosen_image, result_dir)
        self.compare_histograms(chosen_image, result_dir)
