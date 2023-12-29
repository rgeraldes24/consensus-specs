from zond2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators
from zond2spec.test.helpers.constants import CAPELLA


if __name__ == "__main__":
    capella_mods = {key: 'zond2spec.test.capella.fork_choice.test_' + key for key in [
        'get_head',
        'on_block',
        'ex_ante',
        'reorg',
        'withholding',
        'get_proposer_head',
        'on_merge_block',
        'should_override_forkchoice_update',
    ]}

    all_mods = {
        CAPELLA: capella_mods,
    }

    run_state_test_generators(runner_name="fork_choice", all_mods=all_mods)