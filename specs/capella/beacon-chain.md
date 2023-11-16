# Capella -- The Beacon Chain

- [Introduction](#introduction)
- [Custom types](#custom-types)
- [Constants](#constants)
  - [Participation flag indices](#participation-flag-indices)
  - [Incentivization weights](#incentivization-weights)
  - [Domain types](#domain-types)
  - [Misc](#misc)
  - [Withdrawal prefixes](#withdrawal-prefixes)
- [Preset](#preset)
  - [Max operations per block](#max-operations-per-block)
  - [Execution](#execution)
  - [Sync committee](#sync-committee)
  - [Withdrawals processing](#withdrawals-processing)
  - [Misc](#misc-1)
  - [Gwei values](#gwei-values)
  - [Time parameters](#time-parameters)
  - [State list lengths](#state-list-lengths)
  - [Rewards and penalties](#rewards-and-penalties)
- [Configuration](#configuration)
  - [Genesis settings](#genesis-settings)
  - [Time parameters](#time-parameters-1)
  - [Validator cycle](#validator-cycle)
  - [Inactivity penalties](#inactivity-penalties)
- [Containers](#containers)
  - [Misc dependencies](#misc-dependencies)
    - [`Fork`](#fork)
    - [`ForkData`](#forkdata)
    - [`Checkpoint`](#checkpoint)
    - [`Validator`](#validator)
    - [`AttestationData`](#attestationdata)
    - [`IndexedAttestation`](#indexedattestation)
    - [`PendingAttestation`](#pendingattestation)
    - [`Zond1Data`](#zond1data)
    - [`HistoricalSummary`](#historicalsummary)
    - [`HistoricalBatch`](#historicalbatch)
    - [`DepositMessage`](#depositmessage)
    - [`DepositData`](#depositdata)
    - [`BeaconBlockHeader`](#beaconblockheader)
    - [`SigningData`](#signingdata)
  - [Executions](#executions)
    - [`ExecutionPayload`](#executionpayload)
    - [`ExecutionPayloadHeader`](#executionpayloadheader)
  - [Beacon operations](#beacon-operations)
    - [`ProposerSlashing`](#proposerslashing)
    - [`AttesterSlashing`](#attesterslashing)
    - [`Attestation`](#attestation)
    - [`Deposit`](#deposit)
    - [`VoluntaryExit`](#voluntaryexit)
    - [`SyncAggregate`](#syncaggregate)
    - [`SyncCommittee`](#synccommittee)
    - [`DilithiumToExecutionChange`](#dilithiumtoexecutionchange)
  - [Beacon blocks](#beacon-blocks)
    - [`BeaconBlockBody`](#beaconblockbody)
    - [`BeaconBlock`](#beaconblock)
  - [Beacon state](#beacon-state)
    - [`BeaconState`](#beaconstate)
  - [Signed envelopes](#signed-envelopes)
    - [`SignedVoluntaryExit`](#signedvoluntaryexit)
    - [`SignedBeaconBlock`](#signedbeaconblock)
    - [`SignedBeaconBlockHeader`](#signedbeaconblockheader)
    - [`SignedDilithiumToExecutionChange`](#signeddilithiumtoexecutionchanges)
- [Helper functions](#helper-functions)
  - [Beacon state accessors](#beacon-state-accessors)
    - [`ConvertToIndexed`](#converttoindexed)
    - [`AttestingIndices`](#attestingindices)

## Introduction

This document represents the specification for the Beacon Chain.

## Custom types

We define the following Python custom types for type hinting and readability:

| Name | SSZ equivalent | Description |
| - | - | - |
| `Slot` | `uint64` | a slot number |
| `Epoch` | `uint64` | an epoch number |
| `CommitteeIndex` | `uint64` | a committee index at a slot |
| `ValidatorIndex` | `uint64` | a validator registry index |
| `Gwei` | `uint64` | an amount in Gwei |
| `Root` | `Bytes32` | a Merkle root |
| `Hash32` | `Bytes32` | a 256-bit hash |
| `Version` | `Bytes4` | a fork version number |
| `DomainType` | `Bytes4` | a domain type |
| `ForkDigest` | `Bytes4` | a digest of the current fork data |
| `Domain` | `Bytes32` | a signature domain |
| `DilithiumPubkey` | `Bytes2592` | a Dilithium public key |
| `DilithiumSignature` | `Bytes4595` | a Dilithium signature |
| `WithdrawalIndex` | `uint64` | an index of a `Withdrawal` |
| `Transaction` | `ByteList[MAX_BYTES_PER_TRANSACTION]` | either a typed transaction envelope or a legacy transaction|
| `ExecutionAddress` | `Bytes20` | Address of account on the execution layer |
| `ParticipationFlags` | `uint8` | a succinct representation of 8 boolean participation flags |

## Constants

The following values are (non-configurable) constants used throughout the specification.

### Participation flag indices

| Name | Value |
| - | - |
| `TIMELY_SOURCE_FLAG_INDEX` | `0` |
| `TIMELY_TARGET_FLAG_INDEX` | `1` |
| `TIMELY_HEAD_FLAG_INDEX` | `2` |

### Incentivization weights

| Name | Value |
| - | - |
| `TIMELY_SOURCE_WEIGHT` | `uint64(14)` |
| `TIMELY_TARGET_WEIGHT` | `uint64(26)` |
| `TIMELY_HEAD_WEIGHT` | `uint64(14)` |
| `SYNC_REWARD_WEIGHT` | `uint64(2)` |
| `PROPOSER_WEIGHT` | `uint64(8)` |
| `WEIGHT_DENOMINATOR` | `uint64(64)` |

*Note*: The sum of the weights equal `WEIGHT_DENOMINATOR`.

### Domain types

| Name | Value |
| - | - |
| `DOMAIN_BEACON_PROPOSER`     | `DomainType('0x00000000')` |
| `DOMAIN_BEACON_ATTESTER`     | `DomainType('0x01000000')` |
| `DOMAIN_RANDAO`              | `DomainType('0x02000000')` |
| `DOMAIN_DEPOSIT`             | `DomainType('0x03000000')` |
| `DOMAIN_VOLUNTARY_EXIT`      | `DomainType('0x04000000')` |
| `DOMAIN_SELECTION_PROOF`     | `DomainType('0x05000000')` |
| `DOMAIN_AGGREGATE_AND_PROOF` | `DomainType('0x06000000')` |
| `DOMAIN_APPLICATION_MASK`    | `DomainType('0x00000001')` |
| `DOMAIN_SYNC_COMMITTEE` | `DomainType('0x07000000')` |
| `DOMAIN_SYNC_COMMITTEE_SELECTION_PROOF` | `DomainType('0x08000000')` |
| `DOMAIN_CONTRIBUTION_AND_PROOF` | `DomainType('0x09000000')` |
| `DOMAIN_DILITHIUM_TO_EXECUTION_CHANGE` | `DomainType('0x0A000000')` |

*Note*: `DOMAIN_APPLICATION_MASK` reserves the rest of the bitspace in `DomainType` for application usage. This means for some `DomainType` `DOMAIN_SOME_APPLICATION`, `DOMAIN_SOME_APPLICATION & DOMAIN_APPLICATION_MASK` **MUST** be non-zero. This expression for any other `DomainType` in the consensus specs **MUST** be zero.

### Misc

| Name | Value |
| - | - |
| `GENESIS_SLOT` | `Slot(0)` |
| `GENESIS_EPOCH` | `Epoch(0)` |
| `FAR_FUTURE_EPOCH` | `Epoch(2**64 - 1)` |
| `BASE_REWARDS_PER_EPOCH` | `uint64(4)` |
| `DEPOSIT_CONTRACT_TREE_DEPTH` | `uint64(2**5)` (= 32) |
| `JUSTIFICATION_BITS_LENGTH` | `uint64(4)` |
| `ENDIANNESS` | `'little'` |
| `PARTICIPATION_FLAG_WEIGHTS` | `[TIMELY_SOURCE_WEIGHT, TIMELY_TARGET_WEIGHT, TIMELY_HEAD_WEIGHT]` |
| `DEPOSIT_CONTRACT_TREE_DEPTH` | `uint64(2**5)` (= 32) |

### Withdrawal prefixes

| Name | Value |
| - | - |
| `DILITHIUM_WITHDRAWAL_PREFIX` | `Bytes1('0x00')` |
| `ZOND1_ADDRESS_WITHDRAWAL_PREFIX` | `Bytes1('0x01')` |

## Preset

*Note*: The below configuration is bundled as a preset: a bundle of configuration variables which are expected to differ
between different modes of operation, e.g. testing, but not generally between different networks.

### Max operations per block

| Name | Value |
| - | - |
| `MAX_PROPOSER_SLASHINGS` | `2**4` (= 16) |
| `MAX_ATTESTER_SLASHINGS` | `2**1` (= 2) |
| `MAX_ATTESTATIONS` | `2**7` (= 128) |
| `MAX_DEPOSITS` | `2**4` (= 16) |
| `MAX_VOLUNTARY_EXITS` | `2**4` (= 16) |
| `MAX_DILITHIUM_TO_EXECUTION_CHANGES` | `2**4` (= 16) |

### Execution

| Name | Value | Description |
| - | - | - |
| `MAX_BYTES_PER_TRANSACTION` | `uint64(2**30)` (= 1,073,741,824) |
| `MAX_TRANSACTIONS_PER_PAYLOAD` | `uint64(2**20)` (= 1,048,576) |
| `BYTES_PER_LOGS_BLOOM` | `uint64(2**8)` (= 256) |
| `MAX_EXTRA_DATA_BYTES` | `2**5` (= 32) |
| `MAX_WITHDRAWALS_PER_PAYLOAD` | `uint64(2**4)` (= 16) | Maximum amount of withdrawals allowed in each payload |

### Sync committee

| Name | Value | Unit | Duration |
| - | - | - | - |
| `SYNC_COMMITTEE_SIZE` | `uint64(2**9)` (= 512) | validators | |
| `EPOCHS_PER_SYNC_COMMITTEE_PERIOD` | `uint64(2**8)` (= 256) | epochs | ~27 hours |

### Withdrawals processing

| Name | Value |
| - | - |
| `MAX_VALIDATORS_PER_WITHDRAWALS_SWEEP` | `16384` (= 2**14 ) |

### Misc

| Name | Value |
| - | - |
| `MAX_COMMITTEES_PER_SLOT` | `uint64(2**6)` (= 64) |
| `TARGET_COMMITTEE_SIZE` | `uint64(2**7)` (= 128) |
| `MAX_VALIDATORS_PER_COMMITTEE` | `uint64(2**11)` (= 2,048) |
| `SHUFFLE_ROUND_COUNT` | `uint64(90)` |
| `HYSTERESIS_QUOTIENT` | `uint64(4)` |
| `HYSTERESIS_DOWNWARD_MULTIPLIER` | `uint64(1)` |
| `HYSTERESIS_UPWARD_MULTIPLIER` | `uint64(5)` |

- For the safety of committees, `TARGET_COMMITTEE_SIZE` exceeds [the recommended minimum committee size of 111](http://web.archive.org/web/20190504131341/https://vitalik.ca/files/Ithaca201807_Sharding.pdf); with sufficient active validators (at least `SLOTS_PER_EPOCH * TARGET_COMMITTEE_SIZE`), the shuffling algorithm ensures committee sizes of at least `TARGET_COMMITTEE_SIZE`. (Unbiasable randomness with a Verifiable Delay Function (VDF) will improve committee robustness and lower the safe minimum committee size.)

### Gwei values

| Name | Value |
| - | - |
| `MIN_DEPOSIT_AMOUNT` | `Gwei(2**0 * 10**9)` (= 1,000,000,000) |
| `MAX_EFFECTIVE_BALANCE` | `Gwei(2**5 * 10**9)` (= 32,000,000,000) |
| `EFFECTIVE_BALANCE_INCREMENT` | `Gwei(2**0 * 10**9)` (= 1,000,000,000) |

### Time parameters

| Name | Value | Unit | Duration |
| - | - | :-: | :-: |
| `MIN_ATTESTATION_INCLUSION_DELAY` | `uint64(2**0)` (= 1) | slots | 12 seconds |
| `SLOTS_PER_EPOCH` | `uint64(2**5)` (= 32) | slots | 6.4 minutes |
| `MIN_SEED_LOOKAHEAD` | `uint64(2**0)` (= 1) | epochs | 6.4 minutes |
| `MAX_SEED_LOOKAHEAD` | `uint64(2**2)` (= 4) | epochs | 25.6 minutes |
| `MIN_EPOCHS_TO_INACTIVITY_PENALTY` | `uint64(2**2)` (= 4) | epochs | 25.6 minutes |
| `EPOCHS_PER_ZOND1_VOTING_PERIOD` | `uint64(2**6)` (= 64) | epochs | ~6.8 hours |
| `SLOTS_PER_HISTORICAL_ROOT` | `uint64(2**13)` (= 8,192) | slots | ~27 hours |

### State list lengths

| Name | Value | Unit | Duration |
| - | - | :-: | :-: |
| `EPOCHS_PER_HISTORICAL_VECTOR` | `uint64(2**16)` (= 65,536) | epochs | ~0.8 years |
| `EPOCHS_PER_SLASHINGS_VECTOR` | `uint64(2**13)` (= 8,192) | epochs | ~36 days |
| `HISTORICAL_ROOTS_LIMIT` | `uint64(2**24)` (= 16,777,216) | historical roots | ~52,262 years |
| `VALIDATOR_REGISTRY_LIMIT` | `uint64(2**40)` (= 1,099,511,627,776) | validators |

### Rewards and penalties

| Name | Value |
| - | - |
| `BASE_REWARD_FACTOR` | `uint64(2**6)` (= 64) |
| `WHISTLEBLOWER_REWARD_QUOTIENT` | `uint64(2**9)` (= 512) |
| `PROPOSER_REWARD_QUOTIENT` | `uint64(2**3)` (= 8) |
| `INACTIVITY_PENALTY_QUOTIENT` | `uint64(2**26)` (= 67,108,864) |
| `MIN_SLASHING_PENALTY_QUOTIENT` | `uint64(2**7)` (= 128) |
| `PROPORTIONAL_SLASHING_MULTIPLIER` | `uint64(1)` |
| `INACTIVITY_PENALTY_QUOTIENT_BELLATRIX` | `uint64(2**24)` (= 16,777,216) |
| `MIN_SLASHING_PENALTY_QUOTIENT_BELLATRIX` | `uint64(2**5)` (= 32) |
| `PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX` | `uint64(3)` |

- The `INACTIVITY_PENALTY_QUOTIENT` equals `INVERSE_SQRT_E_DROP_TIME**2` where `INVERSE_SQRT_E_DROP_TIME := 2**13` epochs (about 36 days) is the time it takes the inactivity penalty to reduce the balance of non-participating validators to about `1/sqrt(e) ~= 60.6%`. Indeed, the balance retained by offline validators after `n` epochs is about `(1 - 1/INACTIVITY_PENALTY_QUOTIENT)**(n**2/2)`; so after `INVERSE_SQRT_E_DROP_TIME` epochs, it is roughly `(1 - 1/INACTIVITY_PENALTY_QUOTIENT)**(INACTIVITY_PENALTY_QUOTIENT/2) ~= 1/sqrt(e)`. Note this value will be upgraded to `2**24` after Phase 0 mainnet stabilizes to provide a faster recovery in the event of an inactivity leak.

- The `PROPORTIONAL_SLASHING_MULTIPLIER` is set to `1` at initial mainnet launch, resulting in one-third of the minimum accountable safety margin in the event of a finality attack. After Phase 0 mainnet stabilizes, this value will be upgraded to `3` to provide the maximal minimum accountable safety margin.

## Configuration

*Note*: The default mainnet configuration values are included here for illustrative purposes.
Defaults for this more dynamic type of configuration are available with the presets in the [`configs`](../../configs) directory.
Testnets and other types of chain instances may use a different configuration.
Testnets and other types of chain instances may use a different configuration.

### Genesis settings

| Name | Value |
| - | - |
| `MIN_GENESIS_ACTIVE_VALIDATOR_COUNT` | `uint64(2**14)` (= 16,384) |
| `MIN_GENESIS_TIME` | `uint64(1606824000)` (Dec 1, 2020, 12pm UTC) |
| `GENESIS_FORK_VERSION` | `Version('0x00000000')` |
| `GENESIS_DELAY` | `uint64(604800)` (7 days) |

### Time parameters

| Name | Value | Unit | Duration |
| - | - | :-: | :-: |
| `SECONDS_PER_SLOT` | `uint64(12)` | seconds | 12 seconds |
| `SECONDS_PER_ZOND1_BLOCK` | `uint64(14)` | seconds | 14 seconds |
| `MIN_VALIDATOR_WITHDRAWABILITY_DELAY` | `uint64(2**8)` (= 256) | epochs | ~27 hours |
| `SHARD_COMMITTEE_PERIOD` | `uint64(2**8)` (= 256) | epochs | ~27 hours |
| `ZOND1_FOLLOW_DISTANCE` | `uint64(2**11)` (= 2,048) | Zond1 blocks | ~8 hours |

### Validator cycle

| Name | Value |
| - | - |
| `EJECTION_BALANCE` | `Gwei(2**4 * 10**9)` (= 16,000,000,000) |
| `MIN_PER_EPOCH_CHURN_LIMIT` | `uint64(2**2)` (= 4) |
| `CHURN_LIMIT_QUOTIENT` | `uint64(2**16)` (= 65,536) |

### Inactivity penalties

| Name | Value | Description |
| - | - | - |
| `INACTIVITY_SCORE_BIAS` | `uint64(2**2)` (= 4) | score points per inactive epoch |
| `INACTIVITY_SCORE_RECOVERY_RATE` | `uint64(2**4)` (= 16) | score points per leak-free epoch | 

## Containers

The following types are [SimpleSerialize (SSZ)](../../ssz/simple-serialize.md) containers.

### Misc dependencies

#### `Fork`

```python
class Fork(Container):
    previous_version: Version
    current_version: Version
    epoch: Epoch  # Epoch of latest fork
```

#### `ForkData`

```python
class ForkData(Container):
    current_version: Version
    genesis_validators_root: Root
```

#### `Checkpoint`

```python
class Checkpoint(Container):
    epoch: Epoch
    root: Root
```

#### `Validator`

```python
class Validator(Container):
    pubkey: DilithiumPubkey
    withdrawal_credentials: Bytes32  # Commitment to pubkey for withdrawals
    effective_balance: Gwei  # Balance at stake
    slashed: boolean
    # Status epochs
    activation_eligibility_epoch: Epoch  # When criteria for activation were met
    activation_epoch: Epoch
    exit_epoch: Epoch
    withdrawable_epoch: Epoch  # When validator can withdraw funds
```

#### `AttestationData`

```python
class AttestationData(Container):
    slot: Slot
    index: CommitteeIndex
    # LMD GHOST vote
    beacon_block_root: Root
    # FFG vote
    source: Checkpoint
    target: Checkpoint
```

#### `IndexedAttestation`

```python
class IndexedAttestation(Container):
    attesting_indices: List[ValidatorIndex, MAX_VALIDATORS_PER_COMMITTEE]
    data: AttestationData
    signatures: List[DilithiumSignature, MAX_VALIDATORS_PER_COMMITTEE] # List size will be the number of validator indices that have voted exactly the same vote.
```

#### `PendingAttestation`

```python
class PendingAttestation(Container):
    aggregation_bits: Bitlist[MAX_VALIDATORS_PER_COMMITTEE]
    data: AttestationData
    inclusion_delay: Slot
    proposer_index: ValidatorIndex
```

#### `Zond1Data`

```python
class Zond1Data(Container):
    deposit_root: Root
    deposit_count: uint64
    block_hash: Hash32
```

#### `HistoricalSummary`

```python
class HistoricalSummary(Container):
    """
    `HistoricalSummary` matches the components of the phase0 `HistoricalBatch`
    making the two hash_tree_root-compatible.
    """
    block_summary_root: Root
    state_summary_root: Root
```

#### `HistoricalBatch`

```python
class HistoricalBatch(Container):
    block_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
    state_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
```

#### `DepositMessage`

```python
class DepositMessage(Container):
    pubkey: DilithiumPubkey
    withdrawal_credentials: Bytes32
    amount: Gwei
```

#### `DepositData`

```python
class DepositData(Container):
    pubkey: DilithiumPubkey
    withdrawal_credentials: Bytes32
    amount: Gwei
    signature: DilithiumSignature  # Signing over DepositMessage
```

#### `BeaconBlockHeader`

```python
class BeaconBlockHeader(Container):
    slot: Slot
    proposer_index: ValidatorIndex
    parent_root: Root
    state_root: Root
    body_root: Root
```

#### `SigningData`

```python
class SigningData(Container):
    object_root: Root
    domain: Domain
```

### Executions

#### `ExecutionPayload`

```python
class ExecutionPayload(Container):
    # Execution block header fields
    parent_hash: Hash32
    fee_recipient: ExecutionAddress  # 'beneficiary' in the yellow paper
    state_root: Bytes32
    receipts_root: Bytes32
    logs_bloom: ByteVector[BYTES_PER_LOGS_BLOOM]
    prev_randao: Bytes32  # 'difficulty' in the yellow paper
    block_number: uint64  # 'number' in the yellow paper
    gas_limit: uint64
    gas_used: uint64
    timestamp: uint64
    extra_data: ByteList[MAX_EXTRA_DATA_BYTES]
    base_fee_per_gas: uint256
    # Extra payload fields
    block_hash: Hash32  # Hash of execution block
    transactions: List[Transaction, MAX_TRANSACTIONS_PER_PAYLOAD]
    withdrawals: List[Withdrawal, MAX_WITHDRAWALS_PER_PAYLOAD]
```

#### `ExecutionPayloadHeader`

```python
class ExecutionPayloadHeader(Container):
    # Execution block header fields
    parent_hash: Hash32
    fee_recipient: ExecutionAddress
    state_root: Bytes32
    receipts_root: Bytes32
    logs_bloom: ByteVector[BYTES_PER_LOGS_BLOOM]
    prev_randao: Bytes32
    block_number: uint64
    gas_limit: uint64
    gas_used: uint64
    timestamp: uint64
    extra_data: ByteList[MAX_EXTRA_DATA_BYTES]
    base_fee_per_gas: uint256
    # Extra payload fields
    block_hash: Hash32  # Hash of execution block
    transactions_root: Root
    withdrawals_root: Root
```

### Beacon operations

#### `AttesterSlashing`

```python
class AttesterSlashing(Container):
    attestation_1: IndexedAttestation
    attestation_2: IndexedAttestation
```

#### `ProposerSlashing`

```python
class ProposerSlashing(Container):
    signed_header_1: SignedBeaconBlockHeader
    signed_header_2: SignedBeaconBlockHeader
```

#### `Attestation`

*Note*: maps are not supported by szz.

```python
class Attestation(Container):
    aggregation_bits: Bitlist[MAX_VALIDATORS_PER_COMMITTEE] # A bitfield representation of validator indices that have voted exactly the same vote
    // the same vote
    data: AttestationData
    signaturesIdxToValidatorIdx: List[uint64, MAX_VALIDATORS_PER_COMMITTEE]
    signatures: List[DilithiumSignature, MAX_VALIDATORS_PER_COMMITTEE] # List size will be the number of validator indices that have voted exactly the same vote.]
```

```python
class AttestationV2(Container):
    aggregation_bits: Bitlist[MAX_VALIDATORS_PER_COMMITTEE] # A bitfield representation of validator indices that have voted exactly the same vote
    // the same vote
    data: AttestationData
    signatures: List[DilithiumSignature, MAX_VALIDATORS_PER_COMMITTEE] # List size will be the number of validator indices that have voted exactly the same vote.
```

#### `Deposit`

```python
class Deposit(Container):
    proof: Vector[Bytes32, DEPOSIT_CONTRACT_TREE_DEPTH + 1]  # Merkle path to deposit root
    data: DepositData
```

#### `VoluntaryExit`

```python
class VoluntaryExit(Container):
    epoch: Epoch  # Earliest epoch when voluntary exit can be processed
    validator_index: ValidatorIndex
```

#### `SyncAggregate`

```python
class SyncAggregate(Container):
    sync_committee_bits: Bitvector[SYNC_COMMITTEE_SIZE]
    sync_committee_signatures: List[DilithiumSignature, SYNC_COMMITTEE_SIZE]
```

#### `SyncCommittee`

```python
class SyncCommittee(Container):
    pubkeys: Vector[DilithiumPubkey, SYNC_COMMITTEE_SIZE]
```

#### `DilithiumToExecutionChange`

```python
class DilithiumToExecutionChange(Container):
    validator_index: ValidatorIndex
    from_dilithium_pubkey: DilithiumPubkey
    to_execution_address: ExecutionAddress
```

#### `Withdrawal`

```python
class Withdrawal(Container):
    index: WithdrawalIndex
    validator_index: ValidatorIndex
    address: ExecutionAddress
    amount: Gwei
```

### Beacon blocks

#### `BeaconBlockBody`

```python
class BeaconBlockBody(Container):
    randao_reveal: DilithiumSignature
    zond1_data: Zond1Data  # Zond1 data vote
    graffiti: Bytes32  # Arbitrary data
    # Operations
    proposer_slashings: List[ProposerSlashing, MAX_PROPOSER_SLASHINGS]
    attester_slashings: List[AttesterSlashing, MAX_ATTESTER_SLASHINGS]
    attestations: List[Attestation, MAX_ATTESTATIONS]
    deposits: List[Deposit, MAX_DEPOSITS]
    voluntary_exits: List[SignedVoluntaryExit, MAX_VOLUNTARY_EXITS]
    sync_aggregate: SyncAggregate
    # Execution
    execution_payload: ExecutionPayload
    dilithium_to_execution_changes: List[SignedDilithiumToExecutionChange, MAX_DILITHIUM_TO_EXECUTION_CHANGES]
```

#### `BeaconBlock`

```python
class BeaconBlock(Container):
    slot: Slot
    proposer_index: ValidatorIndex
    parent_root: Root
    state_root: Root
    body: BeaconBlockBody
```

### Beacon state

#### `BeaconState`

```python
class BeaconState(Container):
    # Versioning
    genesis_time: uint64
    genesis_validators_root: Root
    slot: Slot
    fork: Fork
    # History
    latest_block_header: BeaconBlockHeader
    block_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
    state_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
    historical_roots: List[Root, HISTORICAL_ROOTS_LIMIT] # Frozen in Capella, replaced by historical_summaries
    # Zond1
    zond1_data: Zond1Data
    zond1_data_votes: List[Zond1Data, EPOCHS_PER_ZOND1_VOTING_PERIOD * SLOTS_PER_EPOCH]
    zond_deposit_index: uint64
    # Registry
    validators: List[Validator, VALIDATOR_REGISTRY_LIMIT]
    balances: List[Gwei, VALIDATOR_REGISTRY_LIMIT]
    # Randomness
    randao_mixes: Vector[Bytes32, EPOCHS_PER_HISTORICAL_VECTOR]
    # Slashings
    slashings: Vector[Gwei, EPOCHS_PER_SLASHINGS_VECTOR]  # Per-epoch sums of slashed effective balances
    # Attestations
    previous_epoch_participation: List[ParticipationFlags, VALIDATOR_REGISTRY_LIMIT]
    current_epoch_participation: List[ParticipationFlags, VALIDATOR_REGISTRY_LIMIT]
    # Finality
    justification_bits: Bitvector[JUSTIFICATION_BITS_LENGTH]  # Bit set for every recent justified epoch
    previous_justified_checkpoint: Checkpoint  # Previous epoch snapshot
    current_justified_checkpoint: Checkpoint
    finalized_checkpoint: Checkpoint
    # Inactivity
    inactivity_scores: List[uint64, VALIDATOR_REGISTRY_LIMIT]
    # Sync
    current_sync_committee: SyncCommittee
    next_sync_committee: SyncCommittee
    # Execution
    latest_execution_payload_header: ExecutionPayloadHeader
    # Withdrawals
    next_withdrawal_index: WithdrawalIndex
    next_withdrawal_validator_index: ValidatorIndex
    historical_summaries: List[HistoricalSummary, HISTORICAL_ROOTS_LIMIT]
```

### Signed envelopes

#### `SignedVoluntaryExit`

```python
class SignedVoluntaryExit(Container):
    message: VoluntaryExit
    signature: DilithiumSignature
```

#### `SignedBeaconBlock`

```python
class SignedBeaconBlock(Container):
    message: BeaconBlock
    signature: DilithiumSignature
```

#### `SignedBeaconBlockHeader`

```python
class SignedBeaconBlockHeader(Container):
    message: BeaconBlockHeader
    signature: DilithiumSignature
```

#### `SignedDilithiumToExecutionChange`

```python
class SignedDilithiumToExecutionChange(Container):
    message: DilithiumToExecutionChange
    signature: DilithiumSignature
```

## Helper functions

### Beacon state accessors

#### `ConvertToIndexed`

```python
def get_indexed_attestation(attestation: Attestation, committee Sequence[ValidatorIndex]) -> IndexedAttestation:
    """
    Return the indexed attestation corresponding to ``attestation``.
    """
    attesting_indices = get_attesting_indices(state, attestation.data, attestation.aggregation_bits)

    return IndexedAttestation(
        attesting_indices=sorted(attesting_indices),
        data=attestation.data,
        signature=attestation.signature,
    )
```

#### `AttestingIndices`

```golang
func AttestingIndices(bf bitfield.Bitfield, committee []primitives.ValidatorIndex) ([]uint64, error) {
	if bf.Len() != uint64(len(committee)) {
		return nil, fmt.Errorf("bitfield length %d is not equal to committee length %d", bf.Len(), len(committee))
	}
	indices := make([]uint64, 0, bf.Count())
	for _, idx := range bf.BitIndices() {
		if idx < len(committee) {
			indices = append(indices, uint64(committee[idx]))
		}
	}
	return indices, nil
}
```