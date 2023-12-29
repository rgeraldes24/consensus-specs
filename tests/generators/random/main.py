from zond2spec.test.helpers.constants import CAPELLA
from zond2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators


if __name__ == "__main__":
    capella_mods = {key: 'zond2spec.test.capella.random.test_' + key for key in [
        'random',
    ]}

    all_mods = {
        CAPELLA: capella_mods,
    }

    run_state_test_generators(runner_name="random", all_mods=all_mods)
