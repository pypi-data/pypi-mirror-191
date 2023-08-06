"""
Utilities for Source DAG Factory
"""

# import logging

from ka_utg.log import Log
from ka_utg.str import Str

# Log = logging.getLogger(__name__)


class GroupId:

    @staticmethod
    def sh_group_id_ix(group_id, group_ix):
        """
        Show group_id_ix
        """
        # return f'{group_id}{group_ix}'
        return f'{group_id}_{group_ix}'


class Tg:

    @staticmethod
    def sh_tg(tg):
        """
        Show tg
        """
        # split string by blank and select first item
        return Str.sh_first_item(tg)

    @classmethod
    def sh_tsk(cls, tg, tsk_ix):
        """
        Show tsk
        """
        return f"{cls.sh_tg(tg).replace('tg_', 'tsk_')}__{tsk_ix}"


class Obj:
    """
    Object class
    """
    @staticmethod
    def sh_group_id(item, group_id):
        if "chain" in item:
            if "id" in item['chain']:
                id = item['chain']['id']
                group_id = f"{group_id}_{id}"
                # group_id = f"{group_id}{id}"
        elif "parallel" in item:
            if "id" in item['parallel']:
                id = item['parallel']['id']
                group_id = f"{group_id}_{id}"
                # group_id = f"{group_id}{id}"
        return group_id

    @staticmethod
    def is_chain(obj):
        sw = 'chain' in obj
        Log.debug(f"Dic.is_chain obj = {obj}")
        return sw

    @staticmethod
    def is_parallel(obj):
        sw = 'parallel' in obj
        Log.debug(f"Dic.is_parallel obj = {obj}")
        Log.debug(f"Dic.is_parallel sw = {sw}")
        return sw

    @staticmethod
    def is_cmd_ope(obj):
        """
        object is command-dictionary i.e.: it contains 'command' as key
        """
        return \
            isinstance(obj, dict) and \
            'command' in obj

    @staticmethod
    def is_oth_ope(obj):
        """
        object is id-dictionary i.e.: it contains 'id' as key
        """
        return \
            isinstance(obj, dict) and \
            'id' in obj and \
            'operator' in obj and \
            'command' not in obj

    @staticmethod
    def is_ope(obj):
        """
        object is id-dictionary i.e.: it contains 'id' as key
        """
        return \
            isinstance(obj, dict) and \
            'operator' in obj
