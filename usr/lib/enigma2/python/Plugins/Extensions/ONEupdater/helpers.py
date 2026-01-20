#!/usr/bin/python
# -*- coding: utf-8 -*-
# Helper utilities for ONEupdater E2 - safer downloads, extraction and file operations.

import os
import shutil
import tempfile
import zipfile
import subprocess
from contextlib import contextmanager

def safe_mkdir(path, mode=0o755):
    if not os.path.exists(path):
        os.makedirs(path, mode=mode, exist_ok=True)

def safe_remove(path):
    if not path:
        return
    if os.path.islink(path) or os.path.isfile(path):
        try:
            os.remove(path)
        except OSError:
            pass
    elif os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)

@contextmanager
def tempdir(prefix='ONEupdater_'):
    td = tempfile.mkdtemp(prefix=prefix)
    try:
        yield td
    finally:
        shutil.rmtree(td, ignore_errors=True)

def extract_zip(zip_path, member_path, dest_dir):
    """
    Extract a folder path member_path from zip_path into dest_dir.
    member_path should be a prefix inside the zip (no leading slash).
    """
    member_prefix = member_path.rstrip('/') + '/'
    with zipfile.ZipFile(zip_path, 'r') as z:
        members = [m for m in z.namelist() if m.startswith(member_prefix)]
        if not members:
            raise KeyError("Folder %r not found in %r" % (member_path, zip_path))
        for m in members:
            # Build the destination relative path
            rel_name = os.path.relpath(m, member_prefix)
            target = os.path.join(dest_dir, rel_name) if rel_name != '.' else dest_dir
            if m.endswith('/'): 
                safe_mkdir(target)
                continue
            safe_mkdir(os.path.dirname(target))
            with z.open(m) as src, open(target, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            # attempt to preserve permission bits stored in ZIP (if present)
            try:
                info = z.getinfo(m)
                perm = (info.external_attr >> 16) & 0o777
                if perm:
                    os.chmod(target, perm)
            except Exception:
                pass

def run_command(cmd, timeout=300, check=True, shell=False):
    """
    Run a command safely. cmd can be list or string. Prefer list.
    Returns subprocess.CompletedProcess. Raises CalledProcessError if check and non-zero exit.
    """
    if isinstance(cmd, str) and not shell:
        # If user passed a string but shell=False, shlex-split it
        import shlex
        cmd = shlex.split(cmd)
    proc = subprocess.run(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=timeout)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)
    return proc

def safe_write_ini(path, section, mapping):
    """
    Write an ini file using configparser safely; ensures directory exists.
    section: string, mapping: dict of keys->values
    """
    import configparser
    cfg = configparser.ConfigParser()
    cfg[section] = mapping
    dirpath = os.path.dirname(path)
    safe_mkdir(dirpath)
    with open(path, 'w') as f:
        cfg.write(f)