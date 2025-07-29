from sqlalchemy import create_engine
from urllib.parse import quote_plus
from .config import load_config 

def get_engine(echo: bool = False):
    cfg = load_config()["postgres"]
    
    user     = cfg["user"]
    password = quote_plus(cfg["password"]) 
    host     = cfg["host"]
    port     = cfg["port"]
    db       = cfg["db"]

    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    return create_engine(connection_url, echo=echo)