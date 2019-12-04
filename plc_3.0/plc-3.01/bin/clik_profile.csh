# this code cannot be run directly
# do 'source /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin/clik_profile.csh' from your csh shell or put it in your profile

 

if !($?PATH) then
setenv PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin
else
set newvar=$PATH
set newvar=`echo ${newvar} | sed s@:/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin:@:@g`
set newvar=`echo ${newvar} | sed s@:/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin\$@@` 
set newvar=`echo ${newvar} | sed s@^/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin:@@`  
set newvar=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin:${newvar}                     
setenv PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/bin:${newvar} 
endif
if !($?PYTHONPATH) then
setenv PYTHONPATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages
else
set newvar=$PYTHONPATH
set newvar=`echo ${newvar} | sed s@:/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages:@:@g`
set newvar=`echo ${newvar} | sed s@:/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages\$@@` 
set newvar=`echo ${newvar} | sed s@^/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages:@@`  
set newvar=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages:${newvar}                     
setenv PYTHONPATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages:${newvar} 
endif
if !($?DYLD_LIBRARY_PATH) then
setenv DYLD_LIBRARY_PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib
else
set newvar=$DYLD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib:@:@g`
set newvar=`echo ${newvar} | sed s@:/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib\$@@` 
set newvar=`echo ${newvar} | sed s@^/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib:@@`  
set newvar=/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib:${newvar}                     
setenv DYLD_LIBRARY_PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib:${newvar} 
endif
if !($?DYLD_LIBRARY_PATH) then
setenv DYLD_LIBRARY_PATH /usr/local/gfortran/lib
else
set newvar=$DYLD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/usr/local/gfortran/lib:@:@g`
set newvar=`echo ${newvar} | sed s@:/usr/local/gfortran/lib\$@@` 
set newvar=`echo ${newvar} | sed s@^/usr/local/gfortran/lib:@@`  
set newvar=/usr/local/gfortran/lib:${newvar}                     
setenv DYLD_LIBRARY_PATH /usr/local/gfortran/lib:${newvar} 
endif
if !($?DYLD_LIBRARY_PATH) then
setenv DYLD_LIBRARY_PATH /System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current
else
set newvar=$DYLD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current:@:@g`
set newvar=`echo ${newvar} | sed s@:/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current\$@@` 
set newvar=`echo ${newvar} | sed s@^/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current:@@`  
set newvar=/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current:${newvar}                     
setenv DYLD_LIBRARY_PATH /System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Versions/Current:${newvar} 
endif
setenv CLIK_PATH /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01

setenv CLIK_DATA /Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/share/clik

setenv CLIK_PLUGIN rel2015

