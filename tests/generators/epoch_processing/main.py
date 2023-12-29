from zond2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators
from zond2spec.test.helpers.constants import CAPELLA


if __name__ == "__main__":
    capella_mods = {key: 'zond2spec.test.capella.epoch_processing.test_process_' + key for key in [
        'justification_and_finalization',
        'rewards_and_penalties',
        'registry_updates',
        'slashings',
        'zond1_data_reset',
        'effective_balance_updates',
        'slashings_reset',
        'randao_mixes_reset',
        'historical_roots_update',
        'participation_record_updates',
        'inactivity_updates',
        'participation_flag_updates',
        'sync_committee_updates',
        'historical_summaries_update',
    ]}

    all_mods = {
        CAPELLA: capella_mods,
    }

    run_state_test_generators(runner_name="epoch_processing", all_mods=all_mods)
