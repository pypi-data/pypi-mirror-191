from subprocess import Popen, PIPE, CalledProcessError

def subprocess(cmd):
    with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')  # process line here

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

if __name__ == "__main__":
    subprocess(["pipreqs", ".", "--force"])