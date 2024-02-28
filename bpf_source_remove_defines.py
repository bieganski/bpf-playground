#!/usr/bin/env python3

import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def run_shell(cmd: str) -> tuple[str, str]:
    process = subprocess.Popen(cmd, shell=True, universal_newlines=True)
    stdout, stderr = process.communicate()
    if (ecode := process.returncode):
        raise ValueError(f"Command <{cmd.split()[0]}> exited with {ecode}")
    return stdout, stderr


def system_get_boot_config() -> Path:
    kernel_configs = list(Path("/boot").glob("config*"))
    if len(kernel_configs) != 1:
        raise ValueError(f"Was expecting exactly 1 config in /boot, got {len(kernel_configs)}: {kernel_configs}")
    return kernel_configs[0]

def parse_boot_config(cfg: Path) -> list[str]:
    lines = system_get_boot_config().read_text().splitlines()
    lines = [x.strip() for x in lines]
    lines = [x for x in lines if x]
    lines = [x for x in lines if not x.startswith("#")]
    defines_set_to_true = [x[:-2] for x in lines if x[-2:] == "=y"]
    return defines_set_to_true


def main(bpf_c_code: Path = None):
    cfg_path = system_get_boot_config()
    defines_set_to_true = parse_boot_config(cfg_path)
    defines_as_gcc_flags = " -D".join(defines_set_to_true)
    run_shell(f"gcc {defines_as_gcc_flags} -E {bpf_c_code}")


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(usage="XXX")
    # TODO test stdin
    parser.add_argument("-b", "--bpf_c_code", type=Path, required=True, help="- for stdin")

    main(**vars(parser.parse_args()))
