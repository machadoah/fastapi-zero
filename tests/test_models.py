from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapi_zero.models import User, table_registry


def test_create_user():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(
            username='machadoah',
            email='machado@ah.com',
            password='legalzão!@1',
        )

        session.add(user)
        session.commit()

        result = session.scalar(
            select(User).where(User.email == 'machado@ah.com')
        )

    assert result.id == 1
    assert result.username == 'machadoah'
