# ===========================================
# Source Dags Factory for Stresstest Runbooks
# ===========================================
#
# path_in_mask='/data/DB/AIR/APC/FDW/rbk/*.yaml' \
# path_in_mask='/data/DB/AIR/APC/FDW/rbk/str.yaml' \
# path_in_mask='/data/DB/AIR/APC/FDW/rbk/mon01.yaml' \
# path_in_mask='/data/DB/AIR/APC/FDW/rbk/mon09.yaml' \
# dir_in='/data/DB/AIR/APC/FDW/rbk' \
# dag_prefix='rbk' \

/usr/bin/env python3 -m ka_air_dfs.dfs \
\
d_pacmod_curr='{tenant: DB, package: ka_air_dfs, module: dfs}' \
path_in_mask='/data/DB/AIR/APC/FDW/rbk/*r_str*.yaml' \
dir_out_dag_src='/data/DB/AIR/APC/FDW/dags/rbk' \
\
a_tags='[FDW_RBK]' \
sw_cmd_ix=True \
sw_async=False \
sw_debug=False \
\
1>dfs_rbk_str.1 2>dfs_rbk_str.2
