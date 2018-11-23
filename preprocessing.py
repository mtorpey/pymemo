from inspect import getfullargspec


def arg_tuple(func, *args, **kwargs):
    kwargs = kwargs.copy()

    spec = getfullargspec(func)

    # Check for too many arguments
    if len(args) > len(spec.args):
        if spec.varargs is None:
            func(*args, **kwargs)  # throws TypeError with useful message
        else:
            kwargs['*' + spec.varargs] = args[len(spec.args):]  # record varargs

    # Convert args to kwargs
    kwargs.update(dict(zip(spec.args, args)))

    # Remove any default arguments
    if spec.defaults is not None:
        for (arg, val) in zip(spec.args[-len(spec.defaults):], spec.defaults):
            if kwargs.get(arg) == val:
                kwargs.pop(arg)
    if spec.kwonlydefaults is not None:
        for arg in spec.kwonlydefaults:
            if kwargs.get(arg) == spec.kwonlydefaults[arg]:
                kwargs.pop(arg)

    # Return as a tuple
    out = tuple(sorted(kwargs.items()))
    return out