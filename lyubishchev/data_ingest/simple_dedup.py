import os

class Dedup:
    """
    check point of time record saved last time
    """
    dedup_file_path: str

    def __init__(self, dedup_file_path: str) -> None:
        self.dedup_file_path = os.path.abspath(dedup_file_path)

    def get_latest_timestamp(self) -> int:
        if not os.path.exists(self.dedup_file_path):
            open(self.dedup_file_path, 'a').close()
        with open(self.dedup_file_path, "r") as dedup_file:
            s = dedup_file.read()
            if s == '':
                s = '0'
            return int(s)

    def save_latest_timestamp(self, unix_timestamp: int) -> None:
        with open(self.dedup_file_path, "w") as dedup_file:
            dedup_file.write("{timestamp}".format(timestamp=unix_timestamp))


if __name__ == "__main__":
    dedup = Dedup("./latest_timestamp.txt")
    print(dedup.get_latest_timestamp())
    dedup.save_latest_timestamp(1624595910)
    print(dedup.get_latest_timestamp())