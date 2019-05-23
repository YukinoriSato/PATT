# PATT

PATT: Polyhedral compilation-based AuTo Tile size optimizer

Copyright (C) 2018-2019, Yukinori Sato All Rights Reserved.




## PATT contents

PATT is a program to optimize the tile size of loop nests.
+ src : PATT program
  + src/patt.py : PATT main script 
  + src/modes/*_modes.py : Optimizer for each mode
  + src/util/*.py : Utilities for optimizer
+ polybench4.2_mainNit : Benchmark suite (PolyBench)
+ TACO2018 : Sample scripts.  These are used for obtaining the results published at [ACM TACO 2019 paper](https://dl.acm.org/citation.cfm?id=3293449).

For more details, please see [ACM TACO 2019 paper](https://dl.acm.org/citation.cfm?id=3293449).

Here, we provide [the Japanese version of this document](README-j.md).

# Overview

![Overview](patt_overview.jpg)



## System requirements

+ PATT needs llvm clang, polly and python2.
+ We use LLVM5.0.0 for evaluation.
+ Command path to llvm is required.



## Download

    $ git clone https://github.com/YukinoriSato/PATT



## PATT Execution sample No. 1 (Local execution)

Move to a sample program No.1.

    $ cd TACO2018/haswell

Set the number of CPU thread, the path to PATT program, the path to the benchmark program.

```
$ vi run_all.sh
threads=32
CC="PATT/src/patt.py"
SRC_DIR="PATT/polybench4.2_mainNit"
```

Execute sample program No.1.

    $ ./run_all.sh


## PATT Execution sample No. 2 (Remote execution)

PATT suports cross compilation and ssh remote execution, which is useful for evaluating various code in many-core CPUs such as Intel Xeon Phi.  Note that the files and directories of the remote machine are seen exactly the same as the host computer.  Actually, we mount the same directory to the same mount point.

    $ cd TACO2018/remote-ssh

Set the number of CPU thread, the remote compute name, the path to PATT program, the path to the benchmark program.

```
$ vi run_all.sh
threads=64
remote=hostname
CC="PATT/src/patt.py"
SRC_DIR="PATT/polybench4.2_mainNit"
```

Execute the sample scritp.

    $ ./run_all.sh


## Flow of 'run_all.sh'

Optimize executer 'run_all.sh' performs the following processing :
+ Read kernels_info.sh : Get the information of benchmark program
+ Create a condition file : Filename is defined by 'export PATT_SETTING_FILE="patt_setting"'
+ Run src/patt.py : Execute the tile size optimizer
  + Execution at the following code. 'kernel' is a benchmark name. 'rep' is the repeat times.<br>
      `${CC} ${CC_OPTION} ${SRC1} ${SRC2} &> ./result/${kernel}/${mode}_${rep}`
  + 'psize' is the data class of Polybench.
  + When compiling the benchmark program, PATT specifies the tile size with --polly-tile-sizes compile option.
+ Run ./extract_data.py : Create a logfile_extracted by extracting the measurement condition and the execution time from logfile.
+ Run ./align_this_time.py : Create a logfile_extracted_aligned by extracting the execution time from logfile_extracted.


## PATT execution result

About PATT's logfile.
+ result / Kernel / Mode_RepeatNo : Logfile of PATT optimizer program.
+ result / Kernel / Mode_RepeatNo_extracted : Logfile of the measurement condition and the execution time.
+ result / Kernel / Mode_RepeatNo_extracted_aligned : Logfile of the execution time.

Run time is displayed at '[measure] this time'. 9999 means the time less than the best time. 9997 means the error.  

Here, '--polly-tile-sizes' is the actual option that specifys tile sizes for Polly and we find the specified tile sizes from this line.

