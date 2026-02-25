import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Config:
    """Application configuration loaded from environment variables."""
    api_key: str
    secret_key: str
    ca_cert_path: str
    ca_password: str

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        required_vars = {
            "API_KEY": "api_key",
            "SECRET_KEY": "secret_key",
            "CA_CERT_PATH": "ca_cert_path",
            "CA_PASSWORD": "ca_password",
        }

        config_values = {}
        missing_vars = []

        for env_var, field_name in required_vars.items():
            value = os.environ.get(env_var)
            if value is None:
                missing_vars.append(env_var)
            else:
                config_values[field_name] = value

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        return cls(**config_values)


# Global config instance
config = Config.from_env()
