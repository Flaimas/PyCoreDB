from database import async_engine, sync_engine
from models import metadata_obj

def create_tables():
    metadata_obj.create_all(sync_engine)