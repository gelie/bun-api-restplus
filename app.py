from core import create_app, db
from core.models import User, Group

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Group': Group}
