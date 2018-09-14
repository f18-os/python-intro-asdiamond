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


def main():
    print("Welcome to ashell.")

    while True:
        raw_cmd = input("user@machine:dir$ ")
        if raw_cmd.strip() is "q" or "exit":
            print("Goodbye")
            sys.exit(0)
        try:
            ret_code = os.fork()
            if ret_code == 0:  # I am child
                child(raw_cmd)
            else:  # I am parent, fork was ok
                child_pid = os.wait() # wait for child TODO background support
        except OSError as e:
            print(f"fork failed with code: {e}")


# Example:
# ls -a -lh --list => ['ls', '-a', '-lh', '--list']
def tok(val):
    return re.split('\s+', val)


if __name__ == '__main__':
    main()
