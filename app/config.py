from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

	app_name: str = "Webshop POC"
	secret_key: str = Field(default="change-me-secret", validation_alias="SECRET_KEY")
	algorithm: str = "HS256"
	access_token_expire_minutes: int = 60 * 24
	admin_email: str | None = Field(default=None, validation_alias="ADMIN_EMAIL")
	admin_password: str | None = Field(default=None, validation_alias="ADMIN_PASSWORD")
	
	# Kafka Configuration
	kafka_bootstrap_servers: str = Field(default="localhost:9092", validation_alias="KAFKA_BOOTSTRAP_SERVERS")
	kafka_analytics_topic: str = Field(default="webshop-analytics", validation_alias="KAFKA_ANALYTICS_TOPIC")
	kafka_enabled: bool = Field(default=True, validation_alias="KAFKA_ENABLED")


settings = Settings()
