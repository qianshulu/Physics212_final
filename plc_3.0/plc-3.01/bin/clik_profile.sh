# this code cannot be run directly
# do 'source /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin/clik_profile.sh' from your sh shell or put it in your profile

function addvar () {
local tmp="${!1}" ;
tmp="${tmp//:${2}:/:}" ; tmp="${tmp/#${2}:/}" ; tmp="${tmp/%:${2}/}" ;
export $1="${2}:${tmp}" ;
} 

if [ -z "${PATH}" ]; then 
PATH=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin
export PATH
else
addvar PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin
fi
if [ -z "${PYTHONPATH}" ]; then 
PYTHONPATH=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages
export PYTHONPATH
else
addvar PYTHONPATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages
fi
if [ -z "${DYLD_LIBRARY_PATH}" ]; then 
DYLD_LIBRARY_PATH=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib
export DYLD_LIBRARY_PATH
else
addvar DYLD_LIBRARY_PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib
fi
if [ -z "${DYLD_LIBRARY_PATH}" ]; then 
DYLD_LIBRARY_PATH=/usr/local/gfortran/lib
export DYLD_LIBRARY_PATH
else
addvar DYLD_LIBRARY_PATH /usr/local/gfortran/lib
fi
if [ -z "${DYLD_LIBRARY_PATH}" ]; then 
DYLD_LIBRARY_PATH=/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current
export DYLD_LIBRARY_PATH
else
addvar DYLD_LIBRARY_PATH /System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current
fi
CLIK_PATH=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01
export CLIK_PATH

CLIK_DATA=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/share/clik
export CLIK_DATA

CLIK_PLUGIN=rel2015
export CLIK_PLUGIN

