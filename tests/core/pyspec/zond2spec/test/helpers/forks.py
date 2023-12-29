from .constants import (
    # CAPELLA,
    PREVIOUS_FORK_OF,
)


def is_post_fork(a, b) -> bool:
    """
    Returns true if fork a is after b, or if a == b
    """
    if a == b:
        return True

    prev_fork = PREVIOUS_FORK_OF[a]
    if prev_fork == b:
        return True
    elif prev_fork is None:
        return False
    else:
        return is_post_fork(prev_fork, b)

# def is_post_capella(spec):
#     return is_post_fork(spec.fork, CAPELLA)
