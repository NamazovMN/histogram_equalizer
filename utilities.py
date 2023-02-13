import argparse
import os.path


def collect_arguments() -> argparse.Namespace:
    """
    Function is utilized to collect user-defined parameters
    :return: Namespace object in which user-defined arguments are kept
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--width', type=int, default=150, required=False,
                        help='Specifies desired image width')
    parser.add_argument('--height', type=int, default=150, required=False,
                        help='Specifies desired image height')
    parser.add_argument('--input_dir', type=str, default='dataset', required=False,
                        help='Specifies path to the folder in which images are kept')
    parser.add_argument('--output_dir', type=str, default='results', required=False,
                        help='Specifies path to the folder, image results will be saved')
    parser.add_argument('--sigma', type=float, default=1.0, required=False,
                        help='Specifies sigma value for gaussian filter')
    parser.add_argument('--bins', type=int, default=256, required=False,
                        help='Specifies the number of bins for histogram')

    return parser.parse_args()


def get_parameters() -> dict:
    """
    Method is utilized to collect user-defined arguments in a dictionary
    :return: all required parameters in a dictionary for the project
    """
    arguments = collect_arguments()
    parameters = dict()
    for argument in vars(arguments):
        parameters[argument] = getattr(arguments, argument)
    return parameters


def check_dir(directory: str) -> None:
    """
    Method is utilized to check the existence of the requested directory. In case it does not exist, function creates
    the corresponding directory
    :param directory: path which existences is checked
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
