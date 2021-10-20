import logging, sys

import databases
import sqlalchemy

_logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./answers.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

answers = sqlalchemy.Table(
    "answers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("team", sqlalchemy.String),
    sqlalchemy.Column("problem", sqlalchemy.String),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime)
)

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
                level=loglevel, stream=sys.stderr,
                format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
            )

async def open_app(loglevel = logging.INFO):
    setup_logging(loglevel)

    # Create all tables from scratch.
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)

    await database.connect()

async def close_app():
    await database.disconnect()
