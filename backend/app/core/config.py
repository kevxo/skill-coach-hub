from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Skill Coach Hub"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    AWS_S3_BUCKET: str
    AWS_REGION: str = "us-east-2"

    class Config:
        env_file = ".env"

settings = Settings()

