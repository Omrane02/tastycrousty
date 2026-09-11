from src.modules.health.schema import Health

def get_health() -> Health:
    return Health(status="ok")