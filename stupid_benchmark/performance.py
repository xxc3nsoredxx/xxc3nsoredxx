#! /usr/bin/env python3

from math import log, log10, nan

# Convert GiB to MiB
def gib (g):
    return g*1024

# Convert (h,m,s) into seconds
def sec (h, m, s):
    return h*3600 + m*60 + s

# Calculate the memory aggressiveness metric
def aggr (mib_orig, mib_mem, exec_time):
    return mib_mem / mib_orig

# Calculate the memory effectiveness metric
def eff (mib_orig, mib_mem, exec_time):
    return mib_orig / exec_time

# Normalize the performance metrics
# Each value is taken log_sed
# sed is always at index 3
def norm (perf):
    sed_a, sed_e = perf[3]
    return [(a/sed_a, e/sed_e) for a,e in perf]

# (MiB used, execution time) for awk/nano/sd/sed/vim
stats_5mib = [
    (9.4, 0.40),
    (570, 3),
    (nan, 0.08),
    (7.7, 0.52),
    (445, 9)
]

stats_50mib = [
    (9.4, 3),
    (gib(5.48), 16),
    (gib(1.18), 0.62),
    (7.7, 5),
    (gib(4.22), sec(0,8,59))
]

# awk/nano/sd/sed/vim/vim (estimate)
stats_200mib = [
    (9.4, 15),
    (gib(21.9), 59),
    (gib(2.51), 2),
    (7.7, 20),
    (gib(12.4), sec(1,15,0)),
    (gib(16.4), sec(1,40,0))
]

stats_1gib = [
    (9.4, sec(0,1,17)),
    (nan, nan),
    (gib(8), 12),
    (7.7, sec(0,1,43)),
    (nan, nan),
]

# 5.1 GiB
stats_51gib = [
    (9.4, sec(0,6,33)),
    (nan, nan),
    (gib(39), sec(0,1,2)),
    (7.7, sec(0,8,59)),
    (nan, nan)
]

# (aggressiveness, effectiveness) for awk/nano/sd/sed/vim
perf_5mib = [(aggr(5,*prog), eff(5,*prog)) for prog in stats_5mib]
perf_50mib = [(aggr(50,*prog), eff(50,*prog)) for prog in stats_50mib]
perf_200mib = [(aggr(200,*prog), eff(200,*prog)) for prog in stats_200mib]
perf_1gib = [(aggr(gib(1),*prog), eff(gib(1),*prog)) for prog in stats_1gib]
perf_51gib = [(aggr(gib(5.1),*prog), eff(gib(5.1),*prog)) for prog in stats_51gib]

norm_5mib = norm(perf_5mib)
norm_50mib = norm(perf_50mib)
norm_200mib = norm(perf_200mib)
norm_1gib = norm(perf_1gib)
norm_51gib = norm(perf_51gib)

print(f'{perf_5mib = }')
print(f'{perf_50mib = }')
print(f'{perf_200mib = }')
print(f'{perf_1gib = }')
print(f'{perf_51gib = }')
print()
print(f'{norm_5mib = }')
print(f'{norm_50mib = }')
print(f'{norm_200mib = }')
print(f'{norm_1gib = }')
print(f'{norm_51gib = }')
