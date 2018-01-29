import subprocess


def run_command(cmd, out, err):
    try:
        p = subprocess.Popen(cmd, stdout = out, stderr = err)
    except OSError:
        #  The cmd in this case could not run, skipping
        return None
    else:
        p.wait()
        try:
            out.flush()
        except AttributeError:
            # doesn't do flush
            pass
        try:
            err.flush()
        except AttributeError:
            # doesn't do flush
            pass
        return p


def run_command_output_piped(cmd):
    return run_command(cmd, subprocess.PIPE, subprocess.PIPE)
