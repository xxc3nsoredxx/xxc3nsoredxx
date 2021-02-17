# An Absolutely Stupid Regex Benchmark
A discussion came up about the speed of regex replace in different programs.
Someone said GNU nano was faster than Vim, but that they'd rather use [sd][sd] for basic regex replace since it beats GNU sed too.
I wanted some numbers, so I collected some numbers.
They're not perfect by any means, but I found it to be an interesting torture test.

## Programs Used
* `awk(1)` - GNU awk 5.1.0
* `nano(1)` - GNU nano 5.3
* `sd(1)` - sd 0.7.6
* `sed(1)` - GNU sed 4.8
* `vim(1)` - Vim 8.2
* `bash(1)` - GNU bash 5.0.18
* `top(1)` - procps-ng 3.3.16

## Testing
All testing was done in bash.
Runtime was collected using "real time" from bash's `time` command or approximated using the stopwatch on my phone.
Memory usage was from the "Virtual Memory Size" column in `top(1)`.

### Data
The test itself is simple: create a file with a bunch of text and run a regerx replace on it.
The file was nothing more than a bunch of lines of 'y'.
Generated with:
```bash
yes | pv -s <size> -S > test.txt.<size>
```
File sizes are 5 MiB, 50 MiB, 200 MiB, 1 GiB, 5.1 GiB.
I had originally planned to just do a small run and generated the test file with `yes > test.txt`.
I let it run just a little bit too long, and I now had 5.1 GiB worth of "y\n".
Instead of creating a new file I just went with it and created a handful of smaller files to go along with it.

### Relevant machine specs
* RAM: 32 GiB
* Swap: 32 GiB partition
* CPU: AMD Ryzen 7 PRO 4750U
* Storage: Samsung 970 EVO Plus 1TB NVMe M.2

### awk
The following command was used:
```bash
time awk -e '/y/{print "test"}' test.txt > test.txt.swp && mv test.txt{.swp,}
```
AFAIK, there isn't a way to do in-place edits.

### nano
The following sequence of steps were used:
```
nano test.txt
C-\ M-r y NL test NL a
C-x y NL
```
where `C-x` means `Ctrl-x`, `M-x` means `Alt-x`, `NL` means `Enter`.
Each step was timed on my phone.

### sd
The following command was used:
```bash
time sd y test test.txt
```

### sed
The following command was used:
```bash
time sed -i -e 's/y/test/' test.txt
```

### vim
The following sequence of setps were used:
```
vim test.txt
:%s/y/test/
:wq
```
In some cases, `:wq` was replaced with `:q!`.
Each step was timed on my phone.

## Results
### 5 MiB
#### Runtime
|         | awk    | nano   | sd     | sed    | vim    |
|:-       |:---    |:----   |:--     |:---    |:---    |
| Open    | ---    | <:01   | ---    | ---    | <:01   |
| Replace | ---    | :01    | ---    | ---    | :07    |
| Write   | ---    | <:01   | ---    | ---    | <:01   |
| Total   | :00.40 | <:03\* | :00.08 | :00.52 | <:09\* |
\* Does not account for time taken to enter the commands

#### Memory Usage
|               | awk     | nano    | sd  | sed     | vim      |
|:-             |:---     |:----    |:--  |:---     |:---      |
| After open    | ---     | 249 MiB | --- | ---     | 30.6 MiB |
| After replace | 9.4 MiB | 570 MiB | ??? | 7.7 MiB | 445 MiB  |

### 50 MiB
#### Runtime
|         | awk | nano  | sd     | sed | vim    |
|:-       |:--- |:----  |:--     |:--- |:---    |
| Open    | --- | :03   | ---    | --- | :01    |
| Replace | --- | :11   | ---    | --- | 8:55   |
| Write   | --- | :02   | ---    | --- | :03    |
| Total   | :03 | :16\* | :00.62 | :05 | 8:59\* |
\* Does not account for time taken to enter the commands

#### Memory Usage
|               | awk     | nano    | sd       | sed     | vim      |
|:-             |:---     |:----    |:--       |:---     |:---      |
| After open    | ---     | 2.0 GiB | ---      | ---     | 172 MiB  |
| After replace | 9.4 MiB | 5.48 GiB| 1.18 GiB | 7.7 MiB | 4.22 GiB |

### 200 MiB
#### Runtime
|         | awk | nano  | sd  | sed | vim        |
|:-       |:--- |:----  |:--  |:--- |:---        |
| Open    | --- | :10   | --- | --- | :04        |
| Replace | --- | :42   | --- | --- | >1:15:00   |
| Write   | --- | :07   | --- | --- | :03\*\*    |
| Total   | :15 | :59\* | :02 | :20 | >1:15:00\* |
\* Does not account for time taken to enter the commands

\*\* `:wq!` because replace was interrupted

#### Memory Usage
|               | awk     | nano    | sd       | sed     | vim       |
|:-             |:---     |:----    |:--       |:---     |:---       |
| After open    | ---     | 9.38 GiB| ---      | ---     | 643 MiB   |
| After replace | 9.4 MiB | 21.9 GiB| 2.51 GiB | 7.7 MiB | >12.4 GiB |

I left `vim` running while I went to go eat.
Since it hadn't finished by the time I got back, I hit `C-c` to interrupt it.
The last `test` was 72% of the way into the file.
Extrapolating assuming linear growth, it may have finished in another ~25 minutes and used up at least another 4 GiB of memory.

### 1 GiB
#### Runtime
|         | awk  | nano | sd  | sed  | vim      |
|:-       |:---  |:---- |:--  |:---  |:---      |
| Open    | ---  | 6:15 | --- | ---  | :23      |
| Replace | ---  | NaN  | --- | ---  | >35:00   |
| Write   | ---  | NaN  | --- | ---  | :03\*\*  |
| Total   | 1:17 | NaN  | :12 | 1:43 | >35:00\* |
\* Does not account for time taken to enter the commands

\*\* `:wq!` because replace was interrupted

#### Memory Usage
|               | awk     | nano   | sd    | sed     | vim       |
|:-             |:---     |:----   |:--    |:---     |:---       |
| After open    | ---     | 48 GiB | ---   | ---     | 3.16 GiB  |
| After replace | 9.4 MiB | OOM    | 8 GiB | 7.7 MiB | >11.2 GiB |

I interrupted `vim` at the 35 minute mark because I didn't want to wait.
The last `test` was only 9% of the way into the file.
It would have crossed the 64 GiB limit on available memory and triggered the OOM reaper well before it would have finished.
Although, it would have taken _unbearably_ long for that to happen because it would have been slowed waaaay down because the process would have been actively running from swap.

### 5.1 GiB
#### Runtime
|         | awk  | nano | sd   | sed  | vim         |
|:-       |:---  |:---- |:--   |:---  |:---         |
| Open    | ---  | NaN  | ---  | ---  | 1:47        |
| Replace | ---  | NaN  | ---  | ---  | >12:30:00   |
| Write   | ---  | NaN  | ---  | ---  | 1:00\*\*    |
| Total   | 6:33 | NaN  | 1:02 | 8:59 | >12:30:00\* |
\* Does not account for time taken to enter the commands

\*\* `:wq!` because replace was interrupted

#### Memory Usage
|               | awk     | nano | sd     | sed     | vim      |
|:-             |:---     |:---- |:--     |:---     |:---      |
| After open    | ---     | OOM  | ---    | ---     | 15.8 GiB |
| After replace | 9.4 MiB | OOM  | 39 GiB | 7.7 MiB | >40 GiB  |

At 3 hours in, `vim` had used 29.1 GiB of memory.
30 minutes later processes began entering swap, but `vim` still fit into RAM.
30 more minutes and RAM began overflowing into swap.
At this point I went to sleep and let things run overnight.
After coming back to it in the morning `vim` had only gone up to using 40 GiB of memory because it was running from swap.
I interrupted it and the last `test` was only 7% of the way into the file.

### Performance
The performance metrics are:
```
                                                       (MiB of memory used)
memory aggressiveness = (execution time in seconds) * ----------------------
                                                      (MiB in original file)

                                                 (MiB of memory used)
memory efficiency = (MiB in original file) * ---------------------------
                                             (execution time in seconds)
```

|         | awk  | nano | sd   | sed  | vim         |
|:-       |:---  |:---- |:--   |:---  |:---         |
| 5 MiB   |
| 50 MiB  |
| 200 MiB |
| 1 GiB   |
| 5.1 GiB |


<!-- link refs -->
[sd]: https://github.com/chmln/sd
