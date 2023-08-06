import sys
import warnings

from ka_dfs.dfs.parms import Parms
from ka_dfs.dfs.dfs import DagsFactory

warnings.filterwarnings("ignore")


def main(*args, **kwargs):
    """
    Load portable Variable into airflow database
    """
    DagsFactory.do(sys.argv, sh_parms=Parms.sh)


if __name__ == "__main__":
    main()
