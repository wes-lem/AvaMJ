"""
Conexão com MySQL via SQLAlchemy.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

from backend.config import settings

logger = logging.getLogger(__name__)

# mysql+pymysql://user:password@host:3306/database
# connect_timeout evita travar a página se o MySQL demorar
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280,
    connect_args={"connect_timeout": 5},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency para rotas FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria tabelas no banco (se não existirem). Não derruba o app se o MySQL estiver inacessível."""
    from backend.models import user, gamification, analytics  # noqa: F401
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco conectado e tabelas verificadas.")
    except OperationalError as e:
        logger.warning(
            "MySQL inacessível (tunnel SSH ou serviço?). App sobe mesmo assim. Erro: %s",
            e,
        )
