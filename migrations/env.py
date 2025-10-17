from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. CORREÇÃO: Importe a variável 'app' diretamente de 'main'
# REMOVA: from main import create_app
from main import app # <-- Importa a instância do Flask
from database.db import db 

# Importar todos os modelos garante que o Alembic os veja
from models.ReportModel import ReportModel 
from models.DriverModel import DriverModel
from models.ProductModel import ProductModel
from models.SolicitationModel import SolicitationModel
from models.ClientModel import ClientModel
from models.AdminModel import AdminModel


# --- Configuração Global ---

# 2. Atribuição: Defina 'application' como a instância importada 'app'
application = app

# 3. Definição do target_metadata: Carrega os metadados dentro do contexto do Flask
with application.app_context():
    target_metadata = db.metadata


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# --- Funções de Migração ---

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    
    import os
    alembic_url = os.getenv("DATABASE_URI")
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=alembic_url
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Execução ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()