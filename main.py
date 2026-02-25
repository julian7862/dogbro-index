"""Trading application entry point.

This module serves as a clean entry point, delegating all creation logic
to the factory module following SOLID principles.
"""

from src.app_factory import create_app


def main() -> None:
    """Application entry point.

    Creates and starts the trading service with proper error handling.
    All component creation is delegated to the factory module.
    """
    print("=" * 60)
    print("Trading Application Starting")
    print("=" * 60)

    # Create application using factory
    service = create_app(
        gateway_url='http://localhost:3001',
        simulation=True,
        heartbeat_interval=10
    )

    try:
        service.start()
    except Exception as e:
        print(f"\nFatal error: {e}")
        return
    finally:
        # Ensure cleanup even on unexpected errors
        if service.is_running():
            service.stop()

    print("\n" + "=" * 60)
    print("Trading Application Stopped")
    print("=" * 60)


if __name__ == "__main__":
    main()
