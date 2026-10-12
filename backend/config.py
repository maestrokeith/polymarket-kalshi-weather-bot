"""Configuration settings for the prediction-market research bot."""
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database and API hardening
    DATABASE_URL: str = "sqlite:///./tradingbot.db"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    ADMIN_API_TOKEN: Optional[str] = None

    # Execution safety: these must remain disabled until separately reviewed.
    SIMULATION_MODE: bool = True
    LIVE_TRADING_ENABLED: bool = False

    # Polymarket CLOB. Public market data may be available without credentials.
    POLYMARKET_ENABLED: bool = False
    POLYMARKET_HOST: str = "https://clob.polymarket.com"
    POLYMARKET_CHAIN_ID: int = 137
    POLYMARKET_API_KEY: Optional[str] = None
    POLYMARKET_API_SECRET: Optional[str] = None
    POLYMARKET_API_PASSPHRASE: Optional[str] = None
    # Prefer a local key file; do not place private key material in source control.
    POLYMARKET_PRIVATE_KEY: Optional[str] = None
    POLYMARKET_PRIVATE_KEY_PATH: Optional[str] = None
    POLYMARKET_FUNDER_ADDRESS: Optional[str] = None
    POLYMARKET_SIGNATURE_TYPE: Optional[str] = None

    # Kalshi. Disabled by default; configure DEMO first.
    KALSHI_ENABLED: bool = False
    KALSHI_ENVIRONMENT: str = "demo"
    KALSHI_API_BASE_URL: str = "https://demo-api.kalshi.co/trade-api/v2"
    KALSHI_API_KEY_ID: Optional[str] = None
    KALSHI_PRIVATE_KEY_PATH: Optional[str] = None

    # Weather sources. Open-Meteo's standard non-commercial forecast API needs no key.
    WEATHER_ENABLED: bool = True
    OPEN_METEO_ENABLED: bool = True
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    OPENWEATHER_API_KEY: Optional[str] = None
    WEATHERAPI_API_KEY: Optional[str] = None
    TOMORROW_IO_API_KEY: Optional[str] = None
    NOAA_API_TOKEN: Optional[str] = None
    WEATHER_SCAN_INTERVAL_SECONDS: int = 300
    WEATHER_SETTLEMENT_INTERVAL_SECONDS: int = 1800
    WEATHER_MIN_EDGE_THRESHOLD: float = 0.08
    WEATHER_MAX_ENTRY_PRICE: float = 0.70
    WEATHER_MAX_TRADE_SIZE: float = 100.0
    WEATHER_CITIES: str = "nyc,chicago,miami,los_angeles,denver"

    # Economic data
    FRED_API_KEY: Optional[str] = None
    BLS_API_KEY: Optional[str] = None

    # Crypto market data. Public endpoints often need no credentials; these are optional.
    BTC_PRICE_SOURCE: str = "coinbase"
    COINBASE_API_BASE_URL: str = "https://api.exchange.coinbase.com"
    BINANCE_API_KEY: Optional[str] = None
    BINANCE_API_SECRET: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None

    # AI providers; do not enable paid calls without setting a budget.
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-haiku-latest"
    AI_LOG_ALL_CALLS: bool = True
    AI_DAILY_BUDGET_USD: float = 1.0

    # Optional frontend map token. Never put private secrets in VITE_* variables.
    VITE_MAPBOX_TOKEN: Optional[str] = None

    # Bot/risk settings
    INITIAL_BANKROLL: float = 10000.0
    KELLY_FRACTION: float = 0.15
    SCAN_INTERVAL_SECONDS: int = 60
    SETTLEMENT_INTERVAL_SECONDS: int = 120
    MIN_EDGE_THRESHOLD: float = 0.02
    MAX_ENTRY_PRICE: float = 0.55
    MAX_TRADES_PER_WINDOW: int = 1
    MAX_TOTAL_PENDING_TRADES: int = 20
    DAILY_LOSS_LIMIT: float = 300.0
    MAX_TRADE_SIZE: float = 75.0
    MIN_TIME_REMAINING: int = 60
    MAX_TIME_REMAINING: int = 1800
    WEIGHT_RSI: float = 0.20
    WEIGHT_MOMENTUM: float = 0.35
    WEIGHT_VWAP: float = 0.20
    WEIGHT_SMA: float = 0.15
    WEIGHT_MARKET_SKEW: float = 0.10
    MIN_MARKET_VOLUME: float = 100.0


settings = Settings()
