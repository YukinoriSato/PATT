#!/bin/bash

#llvm and clang 4.0
#export PATH=/home/yuki/yWork/llvm_400/llvm_build/bin:$PATH
#export PATH=/home/yuki/yWork/llvm_20161129/llvm_build/bin:$PATH
#export PATH=/home/yuki/yWork/llvm_20170412/llvm_build/bin:$PATH
#export PATH=/home/yuki/yWork/llvm_latest/llvm_build/bin:$PATH
#export PATH=/home/yuki/yWork/llvm_401/llvm_build/bin:$PATH
#export PATH=/home/yuki/yWork/llvm_latest2/llvm_build/bin:$PATH
export PATH=/home/yukinori/

LD_LIBRARY_PATH=/home/yuki/yWork/llvm_401/llvm_build/lib:$LD_LIBRARY_PATH
#LD_LIBRARY_PATH=/home/yuki/yWork/llvm_latest2/llvm_build/lib:$LD_LIBRARY_PATH

#polly(path to LLVMPolly.so)
#export PATH_TO_POLLY_LIB="/home/work/llvm/llvm_build/lib"
#export PATH_TO_POLLY_LIB="/home/work/llvm-polly-git/llvm_build/lib"

#cmake
export PATH=/home/yuki/yWork/cmake/cmake-3.8.0-Linux-x86_64/bin:$PATH

#scripts
#export PATH=/home/work/yFlow/script:$PATH
#export PATH=/home/yuki/yWork/ydev/script/misc:$PATH
#export PATH=/home/yuki/yWork/ydev/script/static_ws:$PATH
#export PATH=/home/yuki/yWork/ydev/script/tts:$PATH
#export PATH=/home/yuki/yWork/ydev/script/yPollycc/ver1_x:$PATH

#Exana
#source /home/work/ExanaPkg/setupExana.sh
#source /home/work/ExanaPkg/setupExana.sh.ppmem-phi
#source /home/work/ExanaPkg_yuki/setupExana.sh
#source /home/work/ExanaPkg.t2release_yuki/setupExana.sh
source /home/yuki/yWork/ydev/y_exana/setupExana.sh
export PATH=/home/yuki/yWork/ydev/y_exana:$PATH

#icc
source /opt/intel/bin/compilervars.sh intel64

#pip
#export PATH=/home/yuki/.local/bin:$PATH

#orio
export PYTHONPATH=/home/yuki/yWork/orio/build/lib/pythonX.X/site-packages:$PYTHONPATH
export PATH=/home/yuki/yWork/orio/build/bin:$PATH


