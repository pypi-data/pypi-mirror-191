from contextlib import redirect_stdout
from io import StringIO
import inspect
from math import floor, log
from sys import settrace
import logging as log

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s | \033[1m\033[94m py_deco \033[0m | %(message)s",
)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def inactive(func: callable):
    def inner(*args, **kwargs):
        print(f"\nSkipping function {func.__name__}. Decorated with @inactive...")

    return inner


def redirect(func=None, line_print: list = None):
    def decorator(func: callable):
        def inner(*args, **kwargs):
            with StringIO() as buf, redirect_stdout(buf):
                func(*args, **kwargs)
                output = buf.getvalue()
            lines = output.splitlines()
            if line_print is not None:
                for line in lines:
                    line_print.append(line)
            else:
                width = floor(log(len(lines), 10)) + 1
                for i, line in enumerate(lines):
                    i += 1
                    print(
                        f"{i:0{width}}: {line} {inspect.stack()[1][1]} {inspect.stack()[1][2]} "
                    )

        return inner

    if func is None:
        return decorator
    else:
        return decorator(func)


def stacktrace(func=None, exclude_files=[]):
    def tracer_func(frame, event, arg, self=True):

        co = frame.f_code
        line_no = co.co_firstlineno
        func_name = co.co_name
        caller_filename = frame.f_back.f_code.co_filename

        if func_name == "write":
            return  # ignore write() calls from print statements
        for file in exclude_files:
            if file in caller_filename:
                return  # ignore in ipython notebooks
        # print(frame.f_locals)
        # print([arg for arg in frame.f_code.co_varnames])
        args = str(
            tuple(
                [
                    frame.f_locals.get(arg)
                    for arg in frame.f_code.co_varnames
                    # if arg in frame.f_locals.keys()
                ]
            )
        )
        # print(args)
        if args.endswith(",)"):
            # args = args[:-2] + ")"
            args = args.replace(",)", ")")
        if event == "call":
            if "py_deco" in caller_filename.split("/"):
                log.info(f"\033[93mstacktrace starting for {func_name}\033[0m")
            else:
                log.info(
                    f"\tExecuting {func_name}, line {line_no}, from {caller_filename}"
                )

            # print(f"--> Executing: {func_name}{args}")
            return tracer_func
        # elif event == "return":
        #     print(f"--> Returning: {func_name} ")

        return

    def decorator(func: callable):
        def inner(*args, **kwargs):
            settrace(tracer_func)
            func(*args, **kwargs)
            settrace(None)

        return inner

    if func is None:
        # decorator was used like @stacktrace(...)
        return decorator
    else:
        # decorator was used like @stacktrace, without parens
        return decorator(func)
