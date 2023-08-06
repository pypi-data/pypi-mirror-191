import textwrap

from dry_pipe import DryPipe
from test_00_ground_level_tests.pipeline_defs import pipeline_exerciser_func1


def decorator_factory(argument):
    return lambda a: lambda: [argument, a]


@decorator_factory(argument=123)
def zaz(a, b, c, d):
    return f"{a} {b} {c} {d}"


@DryPipe.python_call(tests=[234, 432])
def zozo(a, b, c, test=None):
    return 432

if __name__ == '__main__':
    arg, func = zaz()
    print(func(4,3,2,1))
    print(f"arg={arg}")

    q = zozo()

    print("")

