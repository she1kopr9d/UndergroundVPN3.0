import database.database
import database.models


def create_tables():
    database.models.Base.metadata.drop_all(database.database.sync_engine)
    database.models.Base.metadata.create_all(database.database.sync_engine)
