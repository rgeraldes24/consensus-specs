# Definitions in context.py
CAPELLA = 'capella'


# The helper functions that are used when defining constants
CONSTANT_DEP_SUNDRY_CONSTANTS_FUNCTIONS = '''
def ceillog2(x: int) -> uint64:
    if x < 1:
        raise ValueError(f"ceillog2 accepts only positive values, x={x}")
    return uint64((x - 1).bit_length())


def floorlog2(x: int) -> uint64:
    if x < 1:
        raise ValueError(f"floorlog2 accepts only positive values, x={x}")
    return uint64(x.bit_length() - 1)
'''


ZOND2_SPEC_COMMENT_PREFIX = "zond2spec:"