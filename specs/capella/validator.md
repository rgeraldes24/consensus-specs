# Capella -- Honest Validator

This document describes the expected actions of a "validator" participating in the Zond proof-of-stake protocol.

## TODO

- SyncCommitteeContribution: add signaturesIdxToValidatorIdx?

## Table of contents

- [Constants](#constants)
  - [Misc](#misc)
- [Containers](#containers)
  - [`Zond1Block`](#zond1block)
  - [`AggregateAndProof`](#aggregateandproof)
  - [`SignedAggregateAndProof`](#signedaggregateandproof)
  - [`SyncCommitteeMessage`](#synccommitteemessage)
  - [`SyncCommitteeContribution`](#synccommitteecontribution)
- [Becoming a validator](#becoming-a-validator)

## Constants

### Misc

| Name | Value | Unit | Duration |
| - | - | :-: | :-: |
| `TARGET_AGGREGATORS_PER_COMMITTEE` | `2**4` (= 16) | validators |

## Containers

### `Zond1Block`

```python
class Eth1Block(Container):
    timestamp: uint64
    deposit_root: Root
    deposit_count: uint64
    # All other eth1 block fields
```

### `SyncCommitteeMessage`

```python
class SyncCommitteeMessage(Container):
    # Slot to which this contribution pertains
    slot: Slot
    # Block root for this signature
    beacon_block_root: Root
    # Index of the validator that produced this signature
    validator_index: ValidatorIndex
    # Signature by the validator over the block root of `slot`
    signature: DilithiumSignature
```

### `SyncCommitteeContribution`

```python
class SyncCommitteeContribution(Container):
    # Slot to which this contribution pertains
    slot: Slot
    # Block root for this contribution
    beacon_block_root: Root
    # The subcommittee this contribution pertains to out of the broader sync committee
    subcommittee_index: uint64
    # A bit is set if a signature from the validator at the corresponding
    # index in the subcommittee is present in the `signatures` list.
    participation_bits: Bitvector[SYNC_COMMITTEE_SIZE // SYNC_COMMITTEE_SUBNET_COUNT]
    # Signature(s) by the validator(s) over the block root of `slot`
    signatures: List[DilithiumSignature, SYNC_COMMITTEE_SIZE] # TODO(rgeraldes24): list max size vs size
    signaturesIdxToParticipationIdx: List[DilithiumSignature, SYNC_COMMITTEE_SIZE] # TODO(rgeraldes24): list max size vs size
```
