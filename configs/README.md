# Configurations

This directory contains a set of configurations used for testing, testnets, and mainnet.
A client binary may be compiled for a specific `PRESET_BASE`, 
and then load different configurations around that preset to participate in different networks or tests.

Standard configs:
- [`mainnet.yaml`](./mainnet.yaml): Mainnet configuration
- [`minimal.yaml`](./minimal.yaml): Minimal configuration, used in spec-testing along with the [`minimal`](../presets/minimal) preset.