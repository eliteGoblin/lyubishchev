import sys
from pprint import pprint

from lyubishchev.data_model import Metadata, TimeInterval


def main() -> int:
    print(sys.path)
    m = Metadata()
    pprint(m)
    e = TimeInterval()
    pprint(e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
