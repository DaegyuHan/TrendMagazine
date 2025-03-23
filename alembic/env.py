from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from core.database.orm import Base
from core.config import Config
from domain.user.entity import user
from domain.magazine.entity import magazine
from domain.article.entity import article
from domain.tag.entity import tags
from domain.tag.entity import tag_similarity
from domain.tag.entity import article_tags

# Alembic Config object
config = context.config

# DB URL을 동기식으로 반환하는 함수
def get_sync_url():
    return str(Config.DB_URL).replace('postgresql+asyncpg://', 'postgresql://')

# alembic 설정에 DB URL 적용
config.set_main_option('sqlalchemy.url', get_sync_url())

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata 설정
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")  # config에서 DB URL 가져오기
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
