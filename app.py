from app import app, db  # llamamos al app que es una instancia de flask
from app.models import AppData


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'AppData': AppData}


# if __name__ == '__main__':
#     app.run(debug=False)
