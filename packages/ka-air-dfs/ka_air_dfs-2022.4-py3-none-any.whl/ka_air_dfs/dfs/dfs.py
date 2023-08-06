"""
Utilities for DAG Factory for tasks
"""

import glob
import os.path
# import logging

from ka_utg.args import Args
from ka_utg.com import Com
from ka_utg.log import Log
from ka_utg.obj import Obj
from ka_utg.timer import Timer

from ka_dfs.dfs.fac import DagFac

from ka_dfs.dfs.uts import Obj as UtsObj
from ka_dfs.dfs.uts import Tg as UtsTg

from ka_dfs.dfs.src import Dags as SrcDags
from ka_dfs.dfs.src import Ope as SrcOpe
from ka_dfs.dfs.src import TskGrp as SrcTskGrp
from ka_dfs.dfs.src import TskArr as SrcTskArr

from ka_uts.yaml import Yaml
from ka_uts.json import Json

# Log = logging.getLogger(__name__)


class TskGrpOpe:

    a_parent_group = []
    a_group_id = []
    level = 0

    @staticmethod
    def add_tsk(a_tskgrp, tsk):
        if tsk is None:
            return
        if isinstance(tsk, (list, tuple)):
            for line in tsk:
                a_tskgrp.append(line)
        else:
            a_tskgrp.append(tsk)

    @classmethod
    def set_child_for_list(
          cls, a_tskgrp,
          dag_id, group_id, parent_group, obj, env, sw_chain):
        a_tsk = list()
        cpy_ix = 0
        cpn_ix = 0
        print(f"set_child level = {cls.level}")

        for item in obj:
            if UtsObj.is_chain(item):
                cls.level = cls.level + 1
                tsk = cls.sh_tsk_chain(
                    dag_id, group_id, parent_group, cpy_ix, obj, env)
                a_tskgrp.append(tsk)
                a_tsk.append(tsk)
                fnc = "set_child_for_list.is_chain"
                print("==========================")
                print(f"{fnc} item = {item}")
                print("==========================")
                a_list = Obj.sh_arr(item['chain']['list'])
                _group_id = UtsTg.sh_tg(tsk)
                _parent_group = tsk
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                print(f"{fnc} level = {cls.level}")
                print(f"{fnc} cpy_ix = {cpy_ix}")
                print(f"{fnc} group_id = {group_id}")
                print(f"{fnc} _group_id = {_group_id}")
                print(f"{fnc} _parent_group = {_parent_group}")
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                # cls.a_group_id.append(_group_id)
                # cls.a_parent_group.append(_parent_group)
                cls.a_group_id.append(group_id)
                cls.a_parent_group.append(parent_group)
                cls.set_child(
                    a_tskgrp, dag_id, _group_id, _parent_group,
                    a_list, env, sw_chain=True)
                cpy_ix = cpy_ix + 1
                group_id = cls.a_group_id.pop()
                parent_group = cls.a_parent_group.pop()
                cls.level = cls.level - 1
                print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                print(f"{fnc} level = {cls.level}")
                print(f"{fnc} cpy_ix = {cpy_ix}")
                print(f"{fnc} group_id = {group_id}")
                print(f"{fnc} parent_group = {parent_group}")
                print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
            elif UtsObj.is_parallel(item):
                cls.level = cls.level + 1
                tsk = cls.sh_tsk_parallel(
                    dag_id, group_id, parent_group, cpy_ix, obj, env)
                a_tskgrp.append(tsk)
                a_tsk.append(tsk)
                fnc = "set_child_for_list.is_parallel"
                print("==========================")
                print(f"{fnc} item = {item}")
                print("==========================")
                a_list = Obj.sh_arr(item['parallel']['list'])
                _group_id = UtsTg.sh_tg(tsk)
                _parent_group = tsk
                print("aaaaaaaaaaaaaaaaaaaaaaaaa")
                print(f"{fnc} level = {cls.level}")
                print(f"{fnc} cpy_ix = {cpy_ix}")
                print(f"{fnc} group_id = {group_id}")
                print(f"{fnc} _group_id = {_group_id}")
                print(f"{fnc} _parent_group = {_parent_group}")
                print("aaaaaaaaaaaaaaaaaaaaaaaaa")
                # cls.a_group_id.append(_group_id)
                # cls.a_parent_group.append(_parent_group)
                cls.a_group_id.append(group_id)
                cls.a_parent_group.append(parent_group)
                cls.set_child(
                    a_tskgrp, dag_id, _group_id, _parent_group,
                    a_list, env, sw_chain=False)
                cpy_ix = cpy_ix + 1
                group_id = cls.a_group_id.pop()
                parent_group = cls.a_parent_group.pop()
                cls.level = cls.level - 1
                print("bbbbbbbbbbbbbbbbbbbbbbbbb")
                print(f"{fnc} level = {cls.level}")
                print(f"{fnc} cpy_ix = {cpy_ix}")
                print(f"{fnc} group_id = {group_id}")
                print(f"{fnc} parent_group = {parent_group}")
                print("bbbbbbbbbbbbbbbbbbbbbbbbb")
            elif UtsObj.is_ope(item):
                tsk = cls.sh_tsk_ope(dag_id, parent_group, cpn_ix, item, env)
                if tsk is None:
                    continue
                a_tskgrp.append(tsk)
                a_tsk.append(tsk)
                DagFac.cmd_ix = DagFac.cmd_ix + 1
                cpn_ix = cpn_ix + 1
                fnc = "set_child_for_list.is_ope"
                print("ccccccccccccccccccccccccc")
                print(f"{fnc} cpy_ix = {cpy_ix}")
                print("ccccccccccccccccccccccccc")
            else:
                msg = (
                    f"dag_id: {dag_id}, group_id: {group_id}, obj: {obj}"
                    f"item: {item} is not chain, parallel or cmds"
                )
                Log.warning(msg)
                continue

        if sw_chain:
            chain = SrcTskArr.sh_chain(a_tsk)
            cls.add_tsk(a_tskgrp, chain)

    @classmethod
    def set_child_for_dict(
          cls, a_tskgrp,
          dag_id, group_id, parent_group, item, env, sw_chain=False):
        a_tsk = list()
        cpy_ix = 0
        cpn_ix = 0
        print(f"set_child level = {cls.level}")

        if UtsObj.is_chain(item):
            cls.level = cls.level + 1
            tsk = cls.sh_tsk_chain(
                dag_id, group_id, parent_group, cpy_ix, item, env)
            a_tskgrp.append(tsk)
            a_tsk.append(tsk)
            a_list = Obj.sh_arr(item['chain']['list'])
            _group_id = UtsTg.sh_tg(tsk)
            _parent_group = tsk
            fnc = "set_child_for_dict.is_chain"
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(f"{fnc} level = {cls.level}")
            print(f"{fnc} cpy_ix = {cpy_ix}")
            print(f"{fnc} group_id = {group_id}")
            print(f"{fnc} _group_id = {_group_id}")
            print(f"{fnc} _parent_group = {_parent_group}")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # cls.a_group_id.append(_group_id)
            # cls.a_parent_group.append(_parent_group)
            cls.a_group_id.append(group_id)
            cls.a_parent_group.append(parent_group)
            cls.set_child(
                a_tskgrp, dag_id, _group_id, _parent_group,
                a_list, env, sw_chain=True)
            cpy_ix = cpy_ix + 1
            group_id = cls.a_group_id.pop()
            parent_group = cls.a_parent_group.pop()
            cls.level = cls.level - 1
            print("bbbbbbbbbbbbbbbbbbbbbbbbb")
            print(f"{fnc} level = {cls.level}")
            print(f"{fnc} cpy_ix = {cpy_ix}")
            print(f"{fnc} group_id = {group_id}")
            print(f"{fnc} parent_group = {parent_group}")
            print("bbbbbbbbbbbbbbbbbbbbbbbbb")
        elif UtsObj.is_parallel(item):
            cls.level = cls.level + 1
            tsk = cls.sh_tsk_parallel(
                dag_id, group_id, parent_group, cpy_ix, item, env)
            a_tskgrp.append(tsk)
            a_tsk.append(tsk)
            fnc = "set_child_for_dict.is_parallel"
            print("==========================")
            print(f"{fnc} = {item}")
            print("==========================")
            a_list = Obj.sh_arr(item['parallel']['list'])
            _group_id = UtsTg.sh_tg(tsk)
            _parent_group = tsk
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(f"{fnc} level = {cls.level}")
            print(f"{fnc} cpy_ix = {cpy_ix}")
            print(f"{fnc} group_id = {group_id}")
            print(f"{fnc} _group_id = {_group_id}")
            print(f"{fnc} _parent_group = {_parent_group}")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")

            cls.a_group_id.append(group_id)
            cls.a_parent_group.append(parent_group)
            cls.set_child(
                a_tskgrp, dag_id, _group_id, _parent_group,
                a_list, env, sw_chain=False)
            cpy_ix = cpy_ix + 1
            group_id = cls.a_group_id.pop()
            parent_group = cls.a_parent_group.pop()
            cls.level = cls.level - 1
            print("bbbbbbbbbbbbbbbbbbbbbbbbb")
            print(f"{fnc} = {cls.level}")
            print(f"{fnc} cpy_ix = {cpy_ix}")
            print(f"{fnc} group_id = {group_id}")
            print(f"{fnc} parent_group = {parent_group}")
            print("bbbbbbbbbbbbbbbbbbbbbbbbb")
        elif UtsObj.is_ope(item):
            tsk = cls.sh_tsk_ope(dag_id, parent_group, cpn_ix, item, env)
            if tsk is None:
                return
            a_tskgrp.append(tsk)
            a_tsk.append(tsk)
            DagFac.cmd_ix = DagFac.cmd_ix + 1
            cpn_ix = cpn_ix + 1
            fnc = "set_child_for_dict.is_ope"
            print("ccccccccccccccccccccccccc")
            print(f"{fnc} cpy_ix = {cpy_ix}")
            print("ccccccccccccccccccccccccc")
        else:
            msg = (
                f"dag_id: {dag_id}, group_id: {group_id}, item: {item} "
                f"is not chain, parallel or cmds"
            )
            Log.warning(msg)
            return
        if sw_chain:
            chain = SrcTskArr.sh_chain(a_tsk)
            cls.add_tsk(a_tskgrp, chain)

    @staticmethod
    def sh_tsk_ope(
          dag_id, parent_group, tsk_ix, obj, env):
        return SrcOpe.sh_tsk(dag_id, parent_group, tsk_ix, obj, env)

    @staticmethod
    def sh_tsk_chain(
          dag_id, group_id, parent_group, tsk_ix, obj, env):
        group_id_new = UtsObj.sh_group_id(obj, group_id)
        tsk = SrcTskGrp.create_child(
            group_id_new, parent_group, tsk_ix, env)
        return tsk

    @staticmethod
    def sh_tsk_parallel(
          dag_id, group_id, parent_group, tsk_ix, obj, env):
        group_id_new = UtsObj.sh_group_id(obj, group_id)
        tsk = SrcTskGrp.create_child(
            group_id_new, parent_group, tsk_ix, env)
        return tsk

    @classmethod
    def set_child(
          cls, a_tskgrpope,
          dag_id, group_id, root_group, obj, env=None, sw_chain=False):
        if isinstance(obj, list):
            print("===============================")
            print(f"set_child list obj = {obj}")
            print("===============================")
            cls.set_child_for_list(
                a_tskgrpope,
                dag_id, group_id, root_group, obj, env, sw_chain
            )
        else:
            print("===============================")
            print(f"set_child dict obj = {obj}")
            print("===============================")
            cls.set_child_for_dict(
                a_tskgrpope,
                dag_id, group_id, root_group, obj, env, sw_chain
            )


class TskGrpFactory:
    """
    Task Groups Factory class
    """
    @classmethod
    def make(cls, dag_id, obj):
        Log.Eq.debug("obj", obj)
        group_id_root = f"g_{obj['chain']['id']}"
        root_group = SrcTskGrp.create_root(group_id_root)

        a_tskgrpope = list()
        group_id = "g"
        obj = obj['chain']['list']
        TskGrpOpe.set_child(
            a_tskgrpope,
            dag_id, group_id, root_group, obj, env=None, sw_chain=True
        )
        a_tskgrp = [root_group] + a_tskgrpope
        return a_tskgrp


class DagsFactory:

    @staticmethod
    def sh_dag(obj, **kwargs):
        if obj is None:
            Log.info("obj is None")
        if obj == dict():
            Log.info("obj == {}")
            return None
        if "chain" not in obj:
            Log.info(f"'chain' is not in obj = {obj}")
            return None
        if "id" not in obj["chain"]:
            Log.info("id is not in obj['chain'] = {obj['chain']}")
            return None

        DagFac.cmd_ix = 0
        DagFac.sw_cmd_ix = kwargs.get('sw_cmd_ix')
        print("6666666666666666666666666666")
        print(f"obj = {obj}")
        print("6666666666666666666666666666")
        dag, dag_id = SrcDags.sh_dag(obj, **kwargs)
        tskgrp = TskGrpFactory.make(dag_id, obj)
        dag_tskgrp = [dag] + tskgrp
        return (dag_id, dag_tskgrp)

    @staticmethod
    def yield_obj(**kwargs):
        path_in_mask = kwargs.get('path_in_mask')
        if path_in_mask is not None:
            a_path = glob.glob(path_in_mask)
            for path in a_path:
                extension = os.path.splitext(path)[1][1:]
                if extension == "json":
                    obj = Json.read(path)
                elif extension in ["yaml", "yml"]:
                    obj = Yaml.read(path)
                else:
                    obj = None
                    Log.info(f"wrong extension = {extension} of path = {path}")
                if obj is None:
                    Log.info(f"obj is None for path = {path}")
                else:
                    yield obj

        a_dag_id = kwargs.get('a_dag_id')
        if a_dag_id is not None:
            dir_in = kwargs.get('dir_in')
            for dag_id in a_dag_id:
                path = f"{dir_in}/{dag_id}.yaml"
                obj = Yaml.read(path)
                yield obj

    @classmethod
    def yield_dag_src(cls, **kwargs):
        y_obj = cls.yield_obj(**kwargs)
        for obj in y_obj:
            dag_src = cls.sh_dag(obj, **kwargs)
            if dag_src is not None:
                yield dag_src

    @classmethod
    def make_src(cls, **kwargs):
        y_dag_src = cls.yield_dag_src(**kwargs)
        dir_out_dag_src = kwargs.get('dir_out_dag_src')
        for dag_src in y_dag_src:
            dag_id = dag_src[0]
            a_dag_src = dag_src[1]
            out_path = f"{dir_out_dag_src}/{dag_id}.py"
            with open(out_path, 'w') as fd:
                for line in a_dag_src:
                    print("==========================")
                    print(f"line = {line}")
                    print("==========================")
                    fd.write(line)

    @classmethod
    def do(cls, *args, **kwargs):
        d_eq = Args.Eq.Dic.sh(*args, **kwargs)
        Com.init(**d_eq)

        Timer.start("DagsFactory", "do")
        cls.make_src(**d_eq)
        Timer.end("DagsFactory", "do")
