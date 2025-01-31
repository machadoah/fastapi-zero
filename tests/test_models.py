from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    user = User(
        username='machadoah',
        email='machado@ah.com',
        password='legalzão!@1',
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'machado@ah.com'))

    assert result.id == 1
    assert result.username == 'machadoah'
