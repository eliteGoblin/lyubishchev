from lyubishchev.data_model import DataReader


class ReportGenerator:  # pylint: disable=too-few-public-methods
    data_reader: DataReader

    def __init__(self, data_reader: DataReader):
        self.data_reader = data_reader

    def generate_report(self, file_path: str) -> None:
        raise NotImplementedError
