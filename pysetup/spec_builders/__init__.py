from .capella import CapellaSpecBuilder


spec_builders = {
    builder.fork: builder
    for builder in (
        CapellaSpecBuilder,
    )
}