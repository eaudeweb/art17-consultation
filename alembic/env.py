from alembic import context
from art17.models import db


context.configure(
    connection=db.session.connection(),
    target_metadata=db.metadata,
    transactional_ddl=False,
)

context.run_migrations()

if not context.is_offline_mode():
    db.session.commit()
