import logging
import pathlib
import subprocess
import typing


def prettify_paths(*paths: typing.List[pathlib.Path]):
    cmd = [
        "shfmt",
        "-i",
        "4",
        "-w",
    ]
    paths_as_strings = [str(x.resolve()) for x in paths]
    cmd.extend(paths_as_strings)

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        outs, errs = proc.communicate(timeout=15)
        logging.debug(outs.decode())
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        logging.warning(errs.decode())

    if errs:
        logging.warning(f"failed to run {' '.join(cmd)}, error: {errs.decode()}")
    else:
        logging.debug(f"ran ok: {' '.join(cmd)}")
