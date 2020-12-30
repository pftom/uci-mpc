# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# python
export PYTHON3_ROOT=/opt/_internal/cpython-3.6.0
export PYTHON_ROOT=/opt/_internal/cpython-2.7.11-ucs4
export PATH=$PYTHON3_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$PYTHON3_ROOT/lib:$LD_LIBRARY_PATH
export PATH=$PYTHON_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$PYTHON_ROOT/lib:$LD_LIBRARY_PATH

export PATH=/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-redhat-linux/4.8.3/bin:/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-redhat-linux/4.8.3:$PATH
export LD_LIBRARY_PATH=/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-redhat-linux/4.8.3/lib:/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-redhat-linux/4.8.3/lib64:$LD_LIBRARY_PATH
