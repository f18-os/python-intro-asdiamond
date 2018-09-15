import os
import re
import sys


def child(raw_cmd):
    cmd = tok(raw_cmd)
    # simple single command a
    fname = cmd[0]
    args = cmd  # By convention args[0] is the filename anyways

    for directory in re.split(":", os.environ['PATH']):  # walk the path
        program = f"{directory}/{fname}"
        if os.access(program, os.X_OK):
            os.execve(program, args, os.environ)
        # try:
        #     os.execve(program, args, os.environ)
        # except FileNotFoundError:  # continue walking the path
        #     pass
        # if you've gotten here every execve has failed, successful execs never return
    print(f"command not found {fname}")


# Example:
# ls -a -lh --list => ['ls', '-a', '-lh', '--list']
def tok(val):
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
            child(cmds[0].strip())
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
            child(cmds[0].strip())
        else:  # I am parent, fork was ok
            os.wait()  # wait for child TODO background support
    except OSError as e:
        print(f"fork failed with code: {e}")


def main():
    print("Welcome to ashell.")

    while True:
        raw_cmd = input("user@machine:dir$ ")
        if raw_cmd == "\n":
            continue
        elif raw_cmd.strip() == "q":
            print("Goodbye")
            return
        elif ">" in raw_cmd:
            exec_oredirect_cmd(raw_cmd)
        elif "<" in raw_cmd:
            print("input redirect")
            exec_iredirect_cmd(raw_cmd)
        elif "|" in raw_cmd:
            print("pipe")
        else:  # simple command with no redirect
            try:
                ret_code = os.fork()
                if ret_code == 0:  # I am child
                    child(raw_cmd)
                else:  # I am parent, fork was ok
                    child_pid = os.wait()  # wait for child TODO background support
            except OSError as e:
                print(f"fork failed with code: {e}")


if __name__ == '__main__':
    main()
