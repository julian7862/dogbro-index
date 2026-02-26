"""Application factory module.

This module provides factory functions for creating application components,
following the Factory Pattern and Dependency Inversion Principle.
"""

import os
from src.utils.config import config
from src.gateway.gateway_client import GatewayClient, GatewayConfig
from src.trading.shioaji_client import ShioajiClient, ShioajiConfig
from src.services.trading_service import TradingService


class AppFactory:
    """Application component factory.

    Centralizes creation and configuration of all application components,
    making it easy to swap implementations and manage dependencies.
    """

    @staticmethod
    def create_gateway_client(
        url: str = None,
        reconnection: bool = True
    ) -> GatewayClient:
        """Create and configure Gateway client.

        Args:
            url: Gateway server URL (defaults to GATEWAY_URL env var or localhost)
            reconnection: Enable auto-reconnection

        Returns:
            Configured GatewayClient instance
        """
        # 優先使用傳入的 URL，其次使用環境變數，最後使用 localhost
        if url is None:
            url = os.getenv('GATEWAY_URL', 'http://localhost:3001')

        gateway_config = GatewayConfig(
            url=url,
            reconnection=reconnection
        )
        return GatewayClient(gateway_config)

    @staticmethod
    def create_shioaji_client(
        simulation: bool = True
    ) -> ShioajiClient:
        """Create and configure Shioaji client.

        Args:
            simulation: Enable simulation mode

        Returns:
            Configured ShioajiClient instance
        """
        shioaji_config = ShioajiConfig(
            api_key=config.api_key,
            secret_key=config.secret_key,
            ca_cert_path=config.ca_cert_path,
            ca_password=config.ca_password,
            simulation=simulation
        )
        return ShioajiClient(shioaji_config)

    @staticmethod
    def create_trading_service(
        gateway_url: str = None,
        simulation: bool = True,
        heartbeat_interval: int = 10
    ) -> TradingService:
        """Create and configure Trading service with all dependencies.

        Args:
            gateway_url: Gateway server URL (defaults to GATEWAY_URL env var)
            simulation: Enable Shioaji simulation mode
            heartbeat_interval: Heartbeat interval in seconds

        Returns:
            Configured TradingService instance with injected dependencies
        """
        gateway_client = AppFactory.create_gateway_client(url=gateway_url)
        shioaji_client = AppFactory.create_shioaji_client(simulation=simulation)

        return TradingService(
            gateway_client=gateway_client,
            shioaji_client=shioaji_client,
            heartbeat_interval=heartbeat_interval
        )


# Convenience function for common use case
def create_app(
    gateway_url: str = None,
    simulation: bool = True,
    heartbeat_interval: int = 10
) -> TradingService:
    """Convenience function to create application with default settings.

    Args:
        gateway_url: Gateway server URL (defaults to GATEWAY_URL env var or localhost)
        simulation: Enable Shioaji simulation mode
        heartbeat_interval: Heartbeat interval in seconds

    Returns:
        Configured TradingService ready to start
    """
    return AppFactory.create_trading_service(
        gateway_url=gateway_url,
        simulation=simulation,
        heartbeat_interval=heartbeat_interval
    )
