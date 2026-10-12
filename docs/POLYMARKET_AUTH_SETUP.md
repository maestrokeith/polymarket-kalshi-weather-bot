# Polymarket authentication setup (safe mode)

## Current state

- Public market scanning uses Polymarket's public Gamma API and does not need wallet credentials.
- This repository does not yet contain a verified authenticated CLOB account client or live order executor.
- `SIMULATION_MODE=true` and `LIVE_TRADING_ENABLED=false` must remain in force during setup.
- The added settings are configuration scaffolding only; they do not claim to authenticate a wallet or place orders.

## Credentials

Keep credentials in the local `.env` file or your deployment provider's encrypted secret store. Never commit `.env`, put secrets in frontend variables (for example `VITE_*`), paste secrets into issues/chat, or log their values.

- `POLYMARKET_API_KEY`, `POLYMARKET_API_SECRET`, `POLYMARKET_API_PASSPHRASE`: CLOB API credentials created/derived through the official Polymarket client after wallet signing.
- `POLYMARKET_PRIVATE_KEY`: exported signing key for the account. Treat it like a password that controls funds; never share it.
- `POLYMARKET_FUNDER_ADDRESS`: public address of the account's funder/proxy wallet, as shown in Polymarket settings. It may differ from the signing-key address.
- `POLYMARKET_SIGNATURE_TYPE`: set only after confirming the account wallet type in current official Polymarket documentation. Email/Magic Link proxy accounts commonly use type `1`; do not assume without confirming.
- `POLYMARKET_CHAIN_ID`: Polygon mainnet chain ID, `137`.

Do not manually invent API credentials. Use the official Polymarket client and documentation, locally, to create or derive them. Never share the private key, secret, passphrase, or one-time login code.

## Safe verification sequence

1. Keep `SIMULATION_MODE=true`, `LIVE_TRADING_ENABLED=false`, and `POLYMARKET_ENABLED=false`.
2. Confirm public Gamma market data works using the existing market-fetching modules; this is unauthenticated and should not need a private key.
3. After SDK compatibility is verified, implement a separate read-only authenticated account check using the official client. It must not call order placement or cancellation methods.
4. Add tests for missing/invalid credentials, proxy-wallet configuration, API failures, and ensuring no secret values appear in logs.
5. Only consider execution after a separately reviewed executor, durable fill/position reconciliation, idempotency, restart recovery, risk limits, and end-to-end tests exist. Never allow a dashboard toggle to bypass server-side gates.

## Local configuration check

Run from the repository root after copying `.env.example` to `.env` and entering any needed values locally:

```bash
python -c "from backend.config import settings; print('simulation_mode=', settings.SIMULATION_MODE); print('live_trading_enabled=', settings.LIVE_TRADING_ENABLED); print('polymarket_enabled=', settings.POLYMARKET_ENABLED); print('clob_credentials_present=', all([settings.POLYMARKET_API_KEY, settings.POLYMARKET_API_SECRET, settings.POLYMARKET_API_PASSPHRASE])); print('signing_key_present=', bool(settings.POLYMARKET_PRIVATE_KEY)); print('funder_address_present=', bool(settings.POLYMARKET_FUNDER_ADDRESS))"
```

This prints only boolean readiness flags, not secret values. Credential presence is not proof that authentication succeeded.
