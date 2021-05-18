from src.dataset.drive import Drive
from src.dataset.download import DatasetDownloader


def check_colab():
    from IPython import get_ipython
    is_on_colab = 'google.colab' in str(get_ipython())
    return is_on_colab
