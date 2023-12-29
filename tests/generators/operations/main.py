from zond2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators, combine_mods
from zond2spec.test.helpers.constants import CAPELLA


if __name__ == "__main__":
    capella_mods = {
        **{'sync_aggregate': [
            'zond2spec.test.capella.block_processing.sync_aggregate.test_process_' + key
            for key in ['sync_aggregate', 'sync_aggregate_random']
        ]},
        **{key: 'zond2spec.test.capella.block_processing.test_process_' + key for key in [
            'attestation',
            'attester_slashing',
            'block_header',
            'deposit',
            'deposit_phase0',
            'deposit_altair',
            'deposit_bellatrix',
            'proposer_slashing',
            'voluntary_exit',
            'execution_payload',
            'voluntary_exit',
            'dilithium_to_execution_change',
            'withdrawals',
        ]}
    }

    all_mods = {
        CAPELLA: capella_mods,
    }

    run_state_test_generators(runner_name="operations", all_mods=all_mods)
