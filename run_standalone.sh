# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
#
# A tools to faciliate the parallel running of fluid_encrypted test scrips.
# A test script is EXPECTED to accepted arguments in the following format:
#
# SCRIPT_NAME $ROLE $SERVER $PORT
#   ROLE:    the role of the running party
#   SERVER:  the address of the party discovering service
#   PORT:    the port of the party discovering service
#
# This tool will try to fill the above three argument to the test script,
# so that totally three processes running the script will be started, to
# simulate run of three party in a standalone machine.
#
# Usage of this script:
#
# bash run_standalone.sh TEST_SCRIPT_NAME
#

# modify the following vars according to your environment
PYTHON="python"
REDIS_HOME="/home/aistudio/redis-stable/src"
SERVER="localhost"
PORT=6379


if [ $# -lt 1 ]; then
    usage
fi

SCRIPT=$1
if [ ! -f $SCRIPT ]; then
    echo 'Could not find script of '$SCRIPT
    exit 1
fi

REDIS_BIN=$REDIS_HOME/redis-cli
if [ ! -f $REDIS_BIN ]; then
    echo 'Could not find redis cli in '$REDIS_HOME
    exit 1
fi

# clear the redis cache
$REDIS_BIN -h $SERVER -p $PORT flushall

# remove temp data generated in last time
LOSS_FILE="tmp/uci_loss.*"

if [ "$LOSS_FILE" ]; then
        rm -rf $LOSS_FILE
fi



# kick off script with roles of 1 and 2, and redirect output to /dev/null
$PYTHON $SCRIPT 1 $SERVER $PORT 2>&1 >/dev/null &
$PYTHON $SCRIPT 2 $SERVER $PORT 2>&1 >/dev/null &

# for party of role 0, run in a foreground mode and show the output
$PYTHON $SCRIPT 0 $SERVER $PORT