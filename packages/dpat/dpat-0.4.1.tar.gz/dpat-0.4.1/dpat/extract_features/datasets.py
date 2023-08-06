import pathlib

from dlup.data.dataset import ConcatDataset, TiledROIsSlideImageDataset


class PMCHHGTileDataset(ConcatDataset):
    """
    add documentation on how this dataset works
    Args:
        add docstrings for the parameters
    """

    def __init__(self, cfg, path, split, dataset_name, data_source):
        self.path = pathlib.Path(path)
        super().__init__([TiledROIsSlideImageDataset(fn) for fn in self.path.glob("*")])

    def num_samples(self):
        """
        Size of the dataset
        """
        return self.__len__()

    def __getitem__(self, idx: int):
        """
        implement how to load the data corresponding to idx element in the dataset
        from your data source
        """
        tile_dict = ConcatDataset.__getitem__(self, idx)

        return tile_dict["image"]
