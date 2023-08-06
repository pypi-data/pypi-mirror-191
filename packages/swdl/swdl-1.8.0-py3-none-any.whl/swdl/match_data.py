import h5py
import pandas as pd

from .tools import PathLike


class MatchData:
    def __init__(self, match_id: str = ""):
        """An interface to store match data information.

        Provides basic operations on MatchData instances

        Args:
            match_id: The id if the match the data belongs to.
        """
        self.objects: pd.DataFrame = pd.DataFrame()
        self.events: pd.DataFrame = pd.DataFrame()
        self.camera_positions = pd.DataFrame()
        self.match_id = match_id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.objects.equals(other.objects)
                and self.events.equals(other.events)
                and self.camera_positions.equals(other.camera_positions)
                and self.match_id == other.match_id
            )
        return False

    def insert_objects(self, df: pd.DataFrame):
        self.objects = pd.concat([self.objects, df], ignore_index=True)

    def save(self, path: PathLike):
        """Save MatchData to hdf5 format.

        The keys 'objects', 'events' and 'camera_positions' will be replaced if writing
            to an exsisting hdf5 file.
        Args:
            path: Path to store the file to.

        """
        self.objects.to_hdf(path, key="objects")
        self.events.to_hdf(path, key="events")
        self.camera_positions.to_hdf(path, key="camera_positions")
        file = h5py.File(path, "a")
        if "meta" not in file.keys():
            ds = file.create_dataset("meta", dtype=int)
        else:
            ds = file["meta"]
        ds.attrs["match_id"] = self.match_id

    def load(self, path: PathLike):
        """Load MatchData from hdf5 file.

        Overwrites the local members inplace.

        Args:
            path: Path to file to load from.
        """
        self.objects = pd.read_hdf(path, key="objects")
        self.events = pd.read_hdf(path, key="events")
        self.camera_positions = pd.read_hdf(path, key="camera_positions")
        file = h5py.File(path, "r")
        ds = file["meta"]
        self.match_id = ds.attrs["match_id"]

    @classmethod
    def from_file(cls, path: PathLike):
        """Create MatchData from hdf5 file.

        Args:
            path: Path to file to load from.
        """
        match_data = cls()
        match_data.load(path)
        return match_data
