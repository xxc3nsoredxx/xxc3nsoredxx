# An Absolutely Stupid Regex Benchmark
A discussion came up about the speed of regex replace in different programs.
Someone said GNU nano was faster than Vim, but that they'd rather use [sd][sd] for basic regex replace since it beats GNU sed too.
They ran a similar test to this, but I wanted my own numbers, so I collected my own numbers.
It's not perfect by any means, but I found this to be an interesting torture test.

## Programs Used
* `awk` - GNU awk 5.1.0
* `nano` - GNU nano 5.3
* `sd` - sd 0.7.6
* `sed` - GNU sed 4.8
* `vim` - Vim 8.2
* `bash` - GNU bash 5.0.18
* `top` - procps-ng 3.3.16

## Testing
The test itself is simple: create a file with a bunch of text and run a regex replace on it.
Runtime was collected using "real time" from bash's `time` command or approximated using the stopwatch on my phone.
Memory usage was from the "Virtual Memory Size" column in `top`.
Not all of this memory was necessarily used, but it's what the process wanted, so I'm using it as a worst case.
I ran the tests from largest file to smallest file which is why some of the data for Vim isn't "true data" but rather an estimate.

### Test data
The files were nothing more than a bunch of lines of 'y' generated with:
```bash
yes | pv -s <size> -S > test.txt.<size>
```
File sizes used were 5 MiB, 50 MiB, 200 MiB, 1 GiB, and 5.1 GiB.
I had originally planned to just do a small run and generated the test file with `yes > test.txt`.
I let it run just a little bit too long and had 5.1 GiB of freshly baked "y\n" sitting on my disk.
Instead of creating a new file I just went with it and created a handful of smaller files to go along with it.

### Relevant machine specs
* CPU: AMD Ryzen 7 PRO 4750U
* Memory: 32 GiB RAM + 32 GiB swap partition
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
time sd 'y' 'test' test.txt
```

### sed
The following command was used:
```bash
time sed -i -e 's/y/test/' test.txt
```

### vim
The following sequence of steps were used:
```
vim test.txt
:%s/y/test/
:wq
```
In some cases, `:wq` was replaced with `:q!`.
Each step was timed on my phone.

## Results
| 5 MiB Runtime | awk    | nano   | sd     | sed    | vim    |
|:------------- |:---    |:----   |:--     |:---    |:---    |
| Open          | ---    | <:01   | ---    | ---    | <:01   |
| Replace       | ---    | :01    | ---    | ---    | :07    |
| Write         | ---    | <:01   | ---    | ---    | <:01   |
| Total         | :00.40 | <:03\* | :00.08 | :00.52 | <:09\* |

| 5 MiB Memory Usage | awk     | nano    | sd      | sed     | vim      |
|:------------------ |:---     |:----    |:--      |:---     |:---      |
| After open         | ---     | 249 MiB | ---     | ---     | 30.6 MiB |
| After replace      | 9.4 MiB | 570 MiB | ???\*\* | 7.7 MiB | 445 MiB  |

| 50 MiB Runtime | awk | nano  | sd     | sed | vim    |
|:-------------- |:--- |:----  |:--     |:--- |:---    |
| Open           | --- | :03   | ---    | --- | :01    |
| Replace        | --- | :11   | ---    | --- | 8:55   |
| Write          | --- | :02   | ---    | --- | :03    |
| Total          | :03 | :16\* | :00.62 | :05 | 8:59\* |

| 50 MiB Memory Usage | awk     | nano    | sd       | sed     | vim      |
|:------------------- |:---     |:----    |:--       |:---     |:---      |
| After open          | ---     | 2.0 GiB | ---      | ---     | 172 MiB  |
| After replace       | 9.4 MiB | 5.48 GiB| 1.18 GiB | 7.7 MiB | 4.22 GiB |

| 200 MiB Runtime | awk | nano  | sd  | sed | vim       | vim (estimate) |
|:--------------- |:--- |:----  |:--  |:--- |:---       |:-------------- |
| Open            | --- | :10   | --- | --- | :04       |                |
| Replace         | --- | :42   | --- | --- | >1:15:00  |                |
| Write           | --- | :07   | --- | --- | :03\*\*\* |                |
| Total           | :15 | :59\* | :02 | :20 | >1:15:00  | >1:40:00       |

| 200 MiB Memory Usage | awk     | nano    | sd       | sed     | vim       | vim (estimate) |
|:-------------------- |:---     |:----    |:--       |:---     |:---       |:-------------- |
| After open           | ---     | 9.38 GiB| ---      | ---     | 643 MiB   |                |
| After replace        | 9.4 MiB | 21.9 GiB| 2.51 GiB | 7.7 MiB | >12.4 GiB | >16.4 GiB      |

I left `vim` running while I went to go eat.
Since it hadn't finished by the time I got back, I hit `C-c` to interrupt it.
The last "test" was 72% of the way into the file.
Extrapolating assuming roughly linear growth as more of the file is processed, it may have finished in another ~25 minutes at best and used up at least another 4 GiB of memory.

| 1 GiB Runtime | awk  | nano | sd  | sed  | vim       |
|:------------- |:---  |:---- |:--  |:---  |:---       |
| Open          | ---  | 6:15 | --- | ---  | :23       |
| Replace       | ---  | NaN  | --- | ---  | >35:00    |
| Write         | ---  | NaN  | --- | ---  | :03\*\*\* |
| Total         | 1:17 | NaN  | :12 | 1:43 | >35:00\*  |

| 1 GiB Memory Usage | awk     | nano   | sd    | sed     | vim       |
|:------------------ |:---     |:----   |:--    |:---     |:---       |
| After open         | ---     | 48 GiB | ---   | ---     | 3.16 GiB  |
| After replace      | 9.4 MiB | OOM    | 8 GiB | 7.7 MiB | >11.2 GiB |

I interrupted `vim` at the 35 minute mark because I didn't want to wait.
The last `test` was only 9% of the way into the file.
It would have crossed the 64 GiB limit on available memory and triggered the OOM reaper well before it would have finished.
Although, it would have taken _unbearably_ long for that to happen because it would have been slowed waaaay down because the process would have been actively running from swap.

| 5.1 GiB Runtime | awk  | nano | sd   | sed  | vim         |
|:--------------- |:---  |:---- |:--   |:---  |:---         |
| Open            | ---  | NaN  | ---  | ---  | 1:47        |
| Replace         | ---  | NaN  | ---  | ---  | >12:30:00   |
| Write           | ---  | NaN  | ---  | ---  | 1:00\*\*\*  |
| Total           | 6:33 | NaN  | 1:02 | 8:59 | >12:30:00\* |

| 5.1 GiB Memory Usage | awk     | nano | sd     | sed     | vim      |
|:-------------------- |:---     |:---- |:--     |:---     |:---      |
| After open           | ---     | OOM  | ---    | ---     | 15.8 GiB |
| After replace        | 9.4 MiB | OOM  | 39 GiB | 7.7 MiB | >40 GiB  |

At 3 hours in, `vim` had used 29.1 GiB of memory.
30 minutes later processes began entering swap, but `vim` still fit into RAM.
30 more minutes and RAM began overflowing into swap.
At this point I went to sleep and let things run overnight.
After coming back to it in the morning `vim` had only gone up to using 40 GiB of memory because it was slowed down due to running from swap.
I interrupted it and the last `test` was only 7% of the way into the file.

| Performance            | awk   | nano   | sd      | vim     | vim (estimate) |
|:-----------            |:---   |:----   |:--      |:---     |:-------------- |
| 5 MiB aggressiveness   | 1.221 | 74.03  | ???\*\* | 57.79   |                |
| 5 MiB effectiveness    | 1.3   | 0.1733 | 6.5     | 0.0578  |                |
| 50 MiB aggressiveness  | 1.221 | 728.8  | 156.9   | 561.2   |                |
| 50 MiB effectiveness   | 1.667 | 0.3125 | 8.065   | 0.0093  |                |
| 200 MiB aggressiveness | 1.221 | 2912   | 333.8   | >1649   | >2181          |
| 200 MiB effectiveness  | 1.333 | 0.3390 | 10.0    | <0.0044 | <0.0033        |
| 1 GiB aggressiveness   | 1.221 | NaN    | 1064    | NaN     |                |
| 1 GiB effectiveness    | 1.338 | NaN    | 8.583   | NaN     |                |
| 5.1 GiB aggressiveness | 1.221 | NaN    | 5186    | NaN     |                |
| 5.1 GiB effectiveness  | 1.372 | NaN    | 8.694   | NaN     |                |

The performance metrics are:
```
                         MiB of memory used
memory aggressiveness = --------------------
                        MiB in original file

                          MiB in original file
memory effectiveness = -------------------------
                       execution time in seconds
```
The results are then normalized by dividing by `sed`'s values.
A higher value means more aggressive memory allocation and more effective memory use, respectively.
Values greater than 1 mean "more than `sed`," and less than 1 mean "less than `sed`."

\* Does not account for time taken to enter the commands.

\*\* `sd` ran too quickly for me to even catch a glimpse of the memory usage in `top`.

\*\*\* `:wq!` because replace was interrupted.

## Conclusion
Both `awk` and `sed` are extremely consistent.
In the test configuration at least, they used the same amount of memory for their internal buffers no matter the size of the input data.
`awk` had a slightly larger buffer than `sed`, and was slightly faster too.
They're standard tools available on pretty much any \*nix system.
They run reasonably fast for reasonable loads.
They can also do a lot more than simple regex replace, but this benchmark isn't testing that.

Nano and Vim fail miserably, but that's unsurprising since they're arguably the wrong tool for the job.
They're designed for editing text not bulk data processing.
Vim's regex features are fantastic, and I use them a lot, but only in the context of normal text editing.
An interesting thing to note is that Vim uses significantly less memory than Nano.

The tool I was most interested in, and the clear winner, is `sd`.
It used _a lot_ of memory, but it also tore right through _a lot_ of data.
The author ran a slightly more scientific `sed` vs `sd` benchmark, but the results were similar to mine.
I'm very impressed and definitely keeping this tool around.
[Here's a link to sd again in case you missed it above.][sd]

<h2><a href='https://github.com/xxc3nsoredxx'><code>return</code></a></h2>


<!-- link refs -->
[sd]: https://github.com/chmln/sd
