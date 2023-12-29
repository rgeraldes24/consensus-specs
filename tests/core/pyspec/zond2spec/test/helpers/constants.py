from .typing import SpecForkName, PresetBaseName


#
# SpecForkName
#

# Some of the Spec module functionality is exposed here to deal with phase-specific changes.
CAPELLA = SpecForkName('capella')

#
# SpecFork settings
#

# The forks that are deployed on Mainnet
MAINNET_FORKS = (CAPELLA)
LATEST_FORK = MAINNET_FORKS[-1]
# The forks that pytest can run with.
# Note: when adding a new fork here, all tests from previous forks with decorator `with_X_and_later`
#       will run on the new fork. To skip this behaviour, add the fork to `ALLOWED_TEST_RUNNER_FORKS`
ALL_PHASES = (
    # Formal forks
    *MAINNET_FORKS,
)
# The forks that have light client specs
LIGHT_CLIENT_TESTING_FORKS = (MAINNET_FORKS)
# The forks that output to the test vectors.
TESTGEN_FORKS = (MAINNET_FORKS)
# Forks allowed in the test runner `--fork` flag, to fail fast in case of typos
ALLOWED_TEST_RUNNER_FORKS = (ALL_PHASES)

# NOTE: the same definition as in `pysetup/md_doc_paths.py`
PREVIOUS_FORK_OF = {
    # post_fork_name: pre_fork_name
    CAPELLA: None,
}

# For fork transition tests
# POST_FORK_OF = {
#     # pre_fork_name: post_fork_name
#}

#
# Config and Preset
#
MAINNET = PresetBaseName('mainnet')
MINIMAL = PresetBaseName('minimal')

ALL_PRESETS = (MINIMAL, MAINNET)


#
# Number
#
MAX_UINT_64 = 2**64 - 1
