# Adding an example

Create a numbered directory under `examples/`. Keep application imports at the SecureAgent boundary, use top-level `.conf` files, reuse `scripts/init-example.sh`, provide `init/run/clean` Make targets, and document the example in its README plus the root index. Do not copy certificate-generation logic into individual examples.
