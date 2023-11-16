# Engine API -- Shanghai

Engine API changes introduced in Shanghai.

- [Structures](#structures)
  - [Withdrawal](#withdrawal)
  - [ExecutionPayload](#executionpayload)
  - [ExecutionPayloadBody](#executionpayloadbody)
  - [PayloadAttributes](#payloadattributes)

## Structures

### Withdrawal

This structure maps onto the validator withdrawal object from the beacon chain spec.
The fields are encoded as follows:

- `index`: `QUANTITY`, 64 Bits
- `validatorIndex`: `QUANTITY`, 64 Bits
- `address`: `DATA`, 20 Bytes
- `amount`: `QUANTITY`, 64 Bits

*Note*: the `amount` value is represented on the beacon chain as a little-endian value in units of Gwei, whereas the
`amount` in this structure *MUST* be converted to a big-endian value in units of Gwei.

### ExecutionPayload

This structure has the syntax of `ExecutionPayload` and appends a single field: `withdrawals`.

- `parentHash`: `DATA`, 32 Bytes
- `feeRecipient`:  `DATA`, 20 Bytes
- `stateRoot`: `DATA`, 32 Bytes
- `receiptsRoot`: `DATA`, 32 Bytes
- `logsBloom`: `DATA`, 256 Bytes
- `prevRandao`: `DATA`, 4595 Bytes
- `blockNumber`: `QUANTITY`, 64 Bits
- `gasLimit`: `QUANTITY`, 64 Bits
- `gasUsed`: `QUANTITY`, 64 Bits
- `timestamp`: `QUANTITY`, 64 Bits
- `extraData`: `DATA`, 0 to 32 Bytes
- `baseFeePerGas`: `QUANTITY`, 256 Bits
- `blockHash`: `DATA`, 32 Bytes
- `transactions`: `Array of DATA` - Array of transaction objects, each object is a byte list (`DATA`) representing `TransactionType || TransactionPayload` or `LegacyTransaction` as defined in [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718)
- `withdrawals`: `Array of Withdrawal` - Array of withdrawals, each object is an `OBJECT` containing the fields of a `Withdrawal` structure.

### ExecutionPayloadBody
This structure contains a body of an execution payload. The fields are encoded as follows:
- `transactions`: `Array of DATA` - Array of transaction objects, each object is a byte list (`DATA`) representing `TransactionType || TransactionPayload` or `LegacyTransaction` as defined in [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718)
- `withdrawals`: `Array of Withdrawal` - Array of withdrawals, each object is an `OBJECT` containing the fields of a `Withdrawal` structure.

### PayloadAttributes

This structure has the syntax of `PayloadAttributes` and appends a single field: `withdrawals`.

- `timestamp`: `QUANTITY`, 64 Bits - value for the `timestamp` field of the new payload
- `prevRandao`: `DATA`, 4595 Bytes - value for the `prevRandao` field of the new payload
- `suggestedFeeRecipient`: `DATA`, 20 Bytes - suggested value for the `feeRecipient` field of the new payload
- `withdrawals`: `Array of Withdrawal` - Array of withdrawals, each object is an `OBJECT` containing the fields of a `Withdrawal` structure.