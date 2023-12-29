from zond2spec.test.helpers.constants import (
    PHASE0,
    PREVIOUS_FORK_OF,
)
from zond2spec.test.helpers.execution_payload import (
    compute_el_header_block_hash,
)
from zond2spec.test.helpers.keys import pubkeys


def build_mock_validator(spec, i: int, balance: int):
    active_pubkey = pubkeys[i]
    withdrawal_pubkey = pubkeys[-1 - i]
    # insecurely use pubkey as withdrawal key as well
    withdrawal_credentials = spec.BLS_WITHDRAWAL_PREFIX + spec.hash(withdrawal_pubkey)[1:]
    validator = spec.Validator(
        pubkey=active_pubkey,
        withdrawal_credentials=withdrawal_credentials,
        activation_eligibility_epoch=spec.FAR_FUTURE_EPOCH,
        activation_epoch=spec.FAR_FUTURE_EPOCH,
        exit_epoch=spec.FAR_FUTURE_EPOCH,
        withdrawable_epoch=spec.FAR_FUTURE_EPOCH,
        effective_balance=min(balance - balance % spec.EFFECTIVE_BALANCE_INCREMENT, spec.MAX_EFFECTIVE_BALANCE)
    )

    return validator


def get_sample_genesis_execution_payload_header(spec,
                                                zond1_block_hash=None):
    if zond1_block_hash is None:
        zond1_block_hash = b'\x55' * 32
    payload_header = spec.ExecutionPayloadHeader(
        parent_hash=b'\x30' * 32,
        fee_recipient=b'\x42' * 20,
        state_root=b'\x20' * 32,
        receipts_root=b'\x20' * 32,
        logs_bloom=b'\x35' * spec.BYTES_PER_LOGS_BLOOM,
        prev_randao=zond1_block_hash,
        block_number=0,
        gas_limit=30000000,
        base_fee_per_gas=1000000000,
        block_hash=zond1_block_hash,
        transactions_root=spec.Root(b'\x56' * 32),
    )

    transactions_trie_root = bytes.fromhex("56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421")
    withdrawals_trie_root = bytes.fromhex("56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421")
    deposit_receipts_trie_root = None
    exits_trie_root = None

    payload_header.block_hash = compute_el_header_block_hash(
        spec,
        payload_header,
        transactions_trie_root,
        withdrawals_trie_root,
        deposit_receipts_trie_root,
        exits_trie_root,
    )
    return payload_header


def create_genesis_state(spec, validator_balances, activation_threshold):
    deposit_root = b'\x42' * 32

    zond1_block_hash = b'\xda' * 32
    previous_version = spec.config.GENESIS_FORK_VERSION
    current_version = spec.config.GENESIS_FORK_VERSION

    if spec.fork != PHASE0:
        previous_fork = PREVIOUS_FORK_OF[spec.fork]
        if previous_fork == PHASE0:
            previous_version = spec.config.GENESIS_FORK_VERSION
        else:
            previous_version = getattr(spec.config, f"{previous_fork.upper()}_FORK_VERSION")
        current_version = getattr(spec.config, f"{spec.fork.upper()}_FORK_VERSION")

    state = spec.BeaconState(
        genesis_time=0,
        zond1_deposit_index=len(validator_balances),
        zond1_data=spec.Zond1Data(
            deposit_root=deposit_root,
            deposit_count=len(validator_balances),
            block_hash=zond1_block_hash,
        ),
        fork=spec.Fork(
            previous_version=previous_version,
            current_version=current_version,
            epoch=spec.GENESIS_EPOCH,
        ),
        latest_block_header=spec.BeaconBlockHeader(body_root=spec.hash_tree_root(spec.BeaconBlockBody())),
        randao_mixes=[zond1_block_hash] * spec.EPOCHS_PER_HISTORICAL_VECTOR,
    )

    # We "hack" in the initial validators,
    #  as it is much faster than creating and processing genesis deposits for every single test case.
    state.balances = validator_balances
    state.validators = [build_mock_validator(spec, i, state.balances[i]) for i in range(len(validator_balances))]

    # Process genesis activations
    for validator in state.validators:
        if validator.effective_balance >= activation_threshold:
            validator.activation_eligibility_epoch = spec.GENESIS_EPOCH
            validator.activation_epoch = spec.GENESIS_EPOCH
        state.previous_epoch_participation.append(spec.ParticipationFlags(0b0000_0000))
        state.current_epoch_participation.append(spec.ParticipationFlags(0b0000_0000))
        state.inactivity_scores.append(spec.uint64(0))
            

    # Set genesis validators root for domain separation and chain versioning
    state.genesis_validators_root = spec.hash_tree_root(state.validators)

    # Fill in sync committees
    # Note: A duplicate committee is assigned for the current and next committee at genesis
    state.current_sync_committee = spec.get_next_sync_committee(state)
    state.next_sync_committee = spec.get_next_sync_committee(state)
        

    # Initialize the execution payload header (with block number and genesis time set to 0)
    state.latest_execution_payload_header = get_sample_genesis_execution_payload_header(
        spec,
        zond1_block_hash=zond1_block_hash,
    )
        
        
    return state
