# Provider keys and setup guide

This file is a credential inventory for the configuration layer. **A variable being present does not mean its provider integration is implemented, authenticated, or enabled.** Confirm each adapter and its tests before relying on it.

## Start with providers that need no secret

| Provider | Environment variables | Key needed? | Use |
|---|---|---:|---|
| Open-Meteo standard forecast API | `OPEN_METEO_ENABLED`, `OPEN_METEO_BASE_URL` | No for standard non-commercial use | Weather forecasts |
| Coinbase Exchange public market data | `BTC_PRICE_SOURCE`, `COINBASE_API_BASE_URL` | No for public endpoints | Crypto reference prices |
| Polymarket public market-data endpoints | `POLYMARKET_HOST` | No for public reads | Public market discovery/prices, depending on endpoint |

Check provider terms, rate limits, and commercial-use restrictions before deploying at scale.

## Account/API credentials

| Provider | Variables | How to obtain them |
|---|---|---|
| Polymarket CLOB | `POLYMARKET_API_KEY`, `POLYMARKET_API_SECRET`, `POLYMARKET_API_PASSPHRASE`, `POLYMARKET_PRIVATE_KEY_PATH`, `POLYMARKET_FUNDER_ADDRESS`, `POLYMARKET_SIGNATURE_TYPE` | Use the official Polymarket account and CLOB documentation. API credentials are created/derived using wallet signing; do not invent them. |
| Kalshi | `KALSHI_API_KEY_ID`, `KALSHI_PRIVATE_KEY_PATH`, `KALSHI_ENVIRONMENT`, `KALSHI_API_BASE_URL` | Create API credentials in Kalshi account settings. Start with the demo environment. Store the private key in a local file and restrict file permissions. |
| FRED | `FRED_API_KEY` | Register/log in through the official FRED API page. |
| U.S. Bureau of Labor Statistics | `BLS_API_KEY` | Register through the official BLS developer/API portal if your intended endpoint or usage requires a key. |
| OpenWeather | `OPENWEATHER_API_KEY` | Create an account and API key through OpenWeather. |
| WeatherAPI | `WEATHERAPI_API_KEY` | Create an account and key through WeatherAPI. |
| Tomorrow.io | `TOMORROW_IO_API_KEY` | Create an account and key through Tomorrow.io. |
| NOAA/NWS | `NOAA_API_TOKEN` | Optional placeholder for endpoints that require an assigned token; verify the specific NOAA endpoint's current authentication requirements first. |
| Binance | `BINANCE_API_KEY`, `BINANCE_API_SECRET` | Only needed for endpoints that require account authentication. Public market data should be preferred where possible. Do not grant withdrawal permissions. |
| CoinGecko | `COINGECKO_API_KEY` | Optional; check current plan and API access before using. |
| Groq | `GROQ_API_KEY` | Create a key in the Groq developer console. Monitor quotas and cost. |
| Anthropic | `ANTHROPIC_API_KEY` | Create a key in the Anthropic Console. Monitor usage and cost. |
| Mapbox | `VITE_MAPBOX_TOKEN` | Create a public/client token in Mapbox. This is frontend-visible; restrict its allowed origins/scopes. Never put private secrets in `VITE_*` variables. |

Official starting points:
- Polymarket docs: https://docs.polymarket.com/
- Polymarket CLOB authentication: https://docs.polymarket.com/developers/CLOB/authentication
- Kalshi docs: https://docs.kalshi.com/
- Kalshi API keys: https://docs.kalshi.com/getting_started/api_keys
- Open-Meteo: https://open-meteo.com/en/docs
- FRED API keys: https://fred.stlouisfed.org/docs/api/api_key.html
- BLS public data API: https://www.bls.gov/developers/
- OpenWeather: https://openweathermap.org/api
- WeatherAPI: https://www.weatherapi.com/
- Tomorrow.io: https://www.tomorrow.io/weather-api/
- NOAA/NWS API: https://www.weather.gov/documentation/services-web-api
- Binance API: https://developers.binance.com/
- CoinGecko API: https://docs.coingecko.com/
- Groq API: https://console.groq.com/docs
- Anthropic API: https://docs.anthropic.com/
- Mapbox tokens: https://docs.mapbox.com/help/dive-deeper/access-tokens/

## Local setup

1. Copy the example file: `cp .env.example .env`.
2. Open `.env` locally and fill only the providers you actually intend to use.
3. Never commit `.env`; check `.gitignore` includes it.
4. For private-key files, keep the key outside the repository and restrict permissions (for example, `chmod 600 /path/to/key.pem`).
5. Never paste secrets into chat, screenshots, logs, GitHub issues, or commits.
6. Test one provider at a time. A non-empty environment variable is not proof of successful authentication.
7. Leave `SIMULATION_MODE=true`, `LIVE_TRADING_ENABLED=false`, `POLYMARKET_ENABLED=false`, and `KALSHI_ENABLED=false` until read-only adapters, error handling, rate limits, and tests are verified.

## Important implementation status

This configuration update adds settings and documentation only. It does **not** itself implement every provider client, perform authentication, fetch provider data, or place orders. Provider adapters should be added and tested separately. Start with unauthenticated public weather/market data, then add authenticated read-only checks. Live order submission should remain a separate, explicitly reviewed milestone.
