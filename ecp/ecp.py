#!/usr/bin/env python

import errno
import os
import struct
import subprocess
import sys
import time

import daemon
import psutil as psutil
from lockfile.pidlockfile import PIDLockFile

import containerizer_pb2

tmp_path = "/tmp/ecp/"

# send() and receive() from http://mesos.apache.org/documentation/latest/external-containerizer/
def receive():
    size = struct.unpack('I', sys.stdin.read(4))
    if size[0] <= 0:
        print >> sys.stderr, "Expected protobuf size over stdin. " \
                             "Received 0 bytes."
        return ""

    data = sys.stdin.read(size[0])
    if len(data) != size[0]:
        print >> sys.stderr, "Expected %d bytes protobuf over stdin. " \
                             "Received %d bytes." % (size[0], len(data))
        return ""
    return data


def send(data):
    sys.stdout.write(struct.pack('I', len(data)))
    sys.stdout.write(data)


def launch_executor(executor, directory):
    with open("%s/stdout" % directory, "a") as stdout_file, open("%s/stderr" % directory, "a") as stderr_file:
        subprocess.check_call(executor, env=os.environ.copy(), stdout=stdout_file, stderr=stderr_file)
    return


def get_pid(container_name):
    pid_file_path = "%s/%s.pid" % (tmp_path, container_name)
    return int(PIDLockFile(pid_file_path).read_pid())


argument = sys.argv[1] if len(sys.argv) > 1 else ""
print >> sys.stderr, "ECP launched with argument: %s" % argument

if argument == "launch":
    launch_message = containerizer_pb2.Launch()
    launch_message.ParseFromString(receive())
    container_name = launch_message.container_id.value
    os.environ['LIBPROCESS_PORT'] = "0"
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    context = daemon.DaemonContext(pidfile=PIDLockFile("%s/%s.pid" % (tmp_path, container_name)))

    # https://pypi.python.org/pypi/python-daemon/ Using python-daemon to implement a well-behaved Unix daemon
    # process because:
    #
    # "Note that launch is not supposed to block. It should return immediately after triggering the
    # executor/command - that could be done via fork-exec within the ECP."
    # from http://mesos.apache.org/documentation/latest/external-containerizer/
    with context:
        launch_executor("/usr/libexec/mesos/mesos-executor", launch_message.directory)
elif argument == "wait":
    def wait_pid(pid):
        # Check every second if process still exists
        try:
            while True:
                # If sig is 0, then no signal is sent, but error checking is still performed;
                # this can be used to check for the existence of a process ID or process group ID.
                os.kill(pid, 0)
                time.sleep(1)
        except OSError as err:
            # If process is not present exit
            if err.errno == errno.ESRCH:
                return


    wait_message = containerizer_pb2.Wait()
    wait_message.ParseFromString(receive())
    container_name = wait_message.container_id.value
    pid = get_pid(container_name)
    # Wait until ECP launch with EX will exit
    wait_pid(pid)
    termination_message = containerizer_pb2.Termination()
    termination_message.killed = False
    termination_message.message = ""
    termination_message.status = 0
    send(termination_message.SerializeToString())
elif argument == "destroy":
    destroy_message = containerizer_pb2.Destroy()
    destroy_message.ParseFromString(receive())
    container_name = destroy_message.container_id.value
    pid = get_pid(container_name)
    os.kill(pid)
elif argument == "containers":
    containers_message = containerizer_pb2.Containers()
    for (_, _, pid_files) in os.walk(tmp_path):
        for pid_file in pid_files:
            pid = int(PIDLockFile("%s/%s" % (tmp_path, pid_file)).read_pid())
            container_id = pid_file[:-4]
            if pid in psutil.pids():
                process = psutil.Process(pid)
                if process.cmdline() == ['python', '/opt/ecp/ecp.py', 'launch']:
                    container = containers_message.containers.add()
                    container.value = container_id
    send(containers_message.SerializeToString())
