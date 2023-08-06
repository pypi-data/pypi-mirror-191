# ==============================
#  Source Dags Factory for Tasks
# ==============================
# 
# path_in_mask='/data/DB/AIR/APC/FDW/tsk/*.yaml' \
# dag_prefix='tsk' \

/usr/bin/env python3 -m ka_air_dfs.dfs \
\
d_pacmod_curr='{tenant: DB, package: ka_air_dfs, module: dfs}' \
path_in_mask='/data/DB/AIR/APC/FDW/tsk/mon/*.yaml' \
dir_out_dag_src='/data/DB/AIR/APC/FDW/dags/tsk/mon' \
\
a_tags='[FDW_TSK]' \
sw_cmd_ix=True \
sw_async=False \
sw_debug=False \
\
1>dfs_tsk.1 2>dfs_tsk.2
