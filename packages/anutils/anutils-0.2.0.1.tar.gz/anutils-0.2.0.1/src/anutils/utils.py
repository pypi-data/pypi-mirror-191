r"""
A.N. 202206
---
general utils.
"""
import datetime
import os
import sys
import time
import warnings

from getkey import getkey


def flatten(lst: list) -> list:
    r"""
    flattens a list of lists or tuples.
    """
    ret = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            ret += flatten(item)
        else:
            ret.append(item)
    return ret


def get_user_choice(prompt: str = 'please confirm', choices: list = None) -> str:
    r"""
    get **one** character from input
    """
    if choices is None:
        choices = ['y', 'n']
    while True:
        if not (prompt.endswith(':') or prompt.endswith(': ')):
            prompt += ':'
        print(f'{prompt} -> [{"/".join(choices)}] ', end='')
        sys.stdout.flush()
        key = getkey()
        print(key, end='')
        if key in choices:
            print()
            break
        else:
            print(' invalid input. ')
            continue
    return key


def print_with_time(string, **kwargs):
    r"""print with time.
    """
    print(f'[{str(datetime.datetime.now())}] {string}', **kwargs)
    sys.stdout.flush()


def silent(mode='all'):
    r"""silent a function.
    params:
        mode: 'all', 'err', 'warn' or 'out'
    """
    def silencer(fn):
        def wrapped(*args, **kwargs):
            oo, oe = sys.stdout, sys.stderr
            with open(os.devnull, 'w', encoding='utf-8') as devnull:
                if mode == 'out':
                    sys.stdout = devnull
                    ret = fn(*args, **kwargs)
                    sys.stdout = oo
                elif mode == 'err':
                    sys.stderr = devnull
                    ret = fn(*args, **kwargs)
                    sys.stderr = oo
                elif mode == 'all':
                    sys.stdout = devnull
                    sys.stderr = devnull
                    ret = fn(*args, **kwargs)
                    sys.stdout, sys.stderr = oo, oe
                elif mode == 'warn':
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        ret = fn(*args, **kwargs)
                else:
                    raise(ValueError(
                        "mode should be in ['out', 'err', 'all', 'warn']"))
            return ret
        return wrapped
    return silencer


def timing(fn, show_datetime: bool = True):
    r"""time a function.
    """
    def timed(*args, **kwargs):
        start = time.time()
        ret = fn(*args, **kwargs)
        tmstr = "{} elapse: {:.3f} s".format(fn.__name__, time.time() - start)
        if show_datetime:
            tmstr = ' '.join(['['+str(datetime.datetime.now())+']', tmstr])
        print(tmstr)
        return ret
    return timed


def logging_to(target_dir: str, need_timing_in_name: bool = False):
    r"""log a function to a file.
    """
    assert os.path.isdir(target_dir)

    def decorator(fn):
        def logged_fn(*args, **kwargs):
            if need_timing_in_name:
                dt = datetime.datetime.now()
                txt_path = os.path.join(target_dir, "log_{:d}_{:d}_{:d}_{:d}_{:d}_{:d}.txt".format(
                    dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
            else:
                txt_path = os.path.join(target_dir, 'log.txt')

            with open(txt_path, 'w', encoding='utf-8') as f:
                old_stdout = sys.stdout
                sys.stdout = f
                ret = fn(*args, **kwargs)
                sys.stdout = old_stdout
            return ret
        return logged_fn
    return decorator


def get_datetime_str() -> str:
    r"""get datetime str.
    """
    dt = datetime.datetime.now()
    dt_str = "{:d}_{:d}_{:d}_{:d}_{:d}_{:d}".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return dt_str
