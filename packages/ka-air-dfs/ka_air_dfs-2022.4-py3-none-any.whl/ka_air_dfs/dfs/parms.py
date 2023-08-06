import warnings

warnings.filterwarnings("ignore")


class Parms:
    """
    Define valid Parameters with default values
    """

    d_eq = {
        "d_pacmod_curr": None,
        "path_in_mask": None,
        "a_dag_id": None,
        "dir_in": None,
        "dir_out_dag_src": None,
        "dag_prefix": None,
        "a_tags": None,
        "sw_cmd_ix": False,
        "sw_async": False,
        "sw_debug": False,
    }

    @classmethod
    def sh(cls):
        """Show Array of valid parameters"""
        return cls.d_eq
