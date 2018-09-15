import os
import re
import sys


def safe_exec(raw_cmd):
    cmd = tok(raw_cmd)
    # simple single command
    fname = cmd[0]
    args = cmd  # By convention args[0] is the filename anyways

    for directory in re.split(":", os.environ['PATH']):  # walk the path
        program = f"{directory}/{fname}"
        if os.access(program, os.X_OK):
            os.execve(program, args, os.environ)
        # if you've gotten here every execve has failed, successful execs never return
    print(f"command not found {fname}")


# Example:
# ls -a -lh --list => ['ls', '-a', '-lh', '--list']
# removes & from strings ls / & => ['ls', '/']
def tok(val):
    val = val.replace("&", "").strip()
    return re.split('\s+', val)


#  for redirecting output of command on left side
#  eg. ls -lh > file.txt
def exec_oredirect_cmd(raw_cmd):
    cmds = re.split(">", raw_cmd)

    try:
        ret_code = os.fork()
        if ret_code == 0:  # I am child
            os.close(sys.stdout.fileno())
            sys.stdout = open(cmds[1].strip(), 'w')
            os.set_inheritable(sys.stdout.fileno(), True)
            safe_exec(cmds[0].strip())
        else:  # I am parent, fork was ok
            child_pid = os.wait()  # wait for child TODO background support
    except OSError as e:
        print(f"fork failed with code: {e}")


#  for redirecting input of command on right side
#  eg. ls -lh < out.txt
def exec_iredirect_cmd(raw_cmd):
    cmds = re.split("<", raw_cmd)

    try:
        ret_code = os.fork()
        if ret_code == 0:  # I am child
            os.close(sys.stdin.fileno())
            sys.stdin = open(cmds[1].strip(), 'r')
            os.set_inheritable(sys.stdin.fileno(), True)
            safe_exec(cmds[0].strip())
        else:  # I am parent, fork was ok
            os.wait()  # wait for child TODO background support
    except OSError as e:
        print(f"fork failed with code: {e}")


def exec_pipe_cmd(raw_cmd):
    producer, consumer = re.split("\|", raw_cmd)
    pipe_out, pipe_in = os.pipe()  # r, w are for reading and writing to the pipe
    try:
        producer_pid = os.fork()
        if producer_pid:  # still parent
            consumer_pid = os.fork()
            if consumer_pid:  # still parent
                os.close(pipe_in)
                os.close(pipe_out)
                os.waitpid(producer_pid, 0)
                os.waitpid(consumer_pid, 0)
            else:  # consumer
                os.dup2(pipe_out, sys.stdin.fileno())
                os.close(pipe_out)
                safe_exec(consumer.strip())
        else:  # producer
            os.dup2(pipe_in, sys.stdout.fileno())
            os.close(pipe_in)
            safe_exec(producer.strip())

    except OSError as e:
        print(f"fork failed with code: {e}")


def exec_bg(raw_cmd):
    pass


def main():
    print("Welcome to ashell.")

    while True:
        try:
            raw_cmd = input("user@machine:dir$ ")
            if raw_cmd == "\n":
                continue
            elif raw_cmd is None:
                continue
            elif raw_cmd == "":
                continue
            elif raw_cmd.strip() == "q":
                return
            elif raw_cmd.strip() == "cd":
                print("chdir")
            elif ">" in raw_cmd:
                exec_oredirect_cmd(raw_cmd)
            elif "<" in raw_cmd:
                exec_iredirect_cmd(raw_cmd)
            elif "|" in raw_cmd:
                exec_pipe_cmd(raw_cmd)
            else:  # simple command with no redirect
                print(f"COMMAND: {raw_cmd}")
                pid = os.fork()
                if pid:  # parent
                    if "&" not in raw_cmd:
                        os.wait()
                else:    # child
                    safe_exec(raw_cmd)
        except EOFError:
            sys.exit()


if __name__ == '__main__':
    main()
