from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    llm_mode: str = "auto"          # off / ft / prompt / auto
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()