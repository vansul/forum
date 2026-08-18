"""
Database configuration and session management for the forum application.

This module provides database engine initialization, session management, and
dependency injection for routers handling users, comments, and posts.
"""

from typing import Generator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Database URL - can be configured via environment variables
# For development, using SQLite with async support
DATABASE_URL = "sqlite+aiosqlite:///./forum.db"


async def init_db_engine() -> AsyncEngine:
    """
    Initialize the async database engine.
    
    Returns:
        AsyncEngine: Configured async SQLAlchemy engine for database operations.
    """
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL query logging
        future=True,
    )
    return engine


async def create_db_and_tables(engine: AsyncEngine) -> None:
    """
    Create database tables based on SQLModel definitions.
    
    Should be called during application startup to ensure all tables exist.
    
    Args:
        engine: The async database engine instance.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_session_factory(engine: AsyncEngine) -> sessionmaker:
    """
    Create a session factory for database operations.
    
    Args:
        engine: The async database engine instance.
        
    Returns:
        sessionmaker: A factory for creating async database sessions.
    """
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_session(
    session_factory: sessionmaker,
) -> Generator[AsyncSession, None, None]:
    """
    Dependency injection function for FastAPI routers to get database sessions.
    
    Usage in routers:
        @router.get("/users")
        async def get_users(session: AsyncSession = Depends(get_session)):
            # Use session for database operations
            pass
    
    Args:
        session_factory: The session factory created by get_session_factory.
        
    Yields:
        AsyncSession: An async database session for router operations.
    """
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
