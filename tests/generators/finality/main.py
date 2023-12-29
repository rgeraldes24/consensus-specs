from zond2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators
from zond2spec.test.helpers.constants import CAPELLA


if __name__ == "__main__":
    capella_mods = {'finality': 'zond2spec.test.capella.finality.test_finality'}

    all_mods = {
        CAPELLA: capella_mods,
    }

    run_state_test_generators(runner_name="finality", all_mods=all_mods)
