from utilities import *
from src.image_read import ReadImages
from src.statistics import Statistics


def __main__():
    """
    Main Function of the project, which orchestrates all tasks
    :return: None
    """
    parameters = get_parameters()
    image_reader = ReadImages(parameters)
    stats = Statistics(parameters, image_reader)
    stats.show_statistics()


if __name__ == '__main__':
    __main__()
