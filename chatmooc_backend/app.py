from flask import Flask
from flask_cors import CORS

from cardfolderEditor import folder_blueprint
from fileEditor import file_blueprint
from flashcardEditor import card_blueprint
from sectionEditor import chapter_blueprint
from LLMrelatedEditor import LLM_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(chapter_blueprint, url_prefix='')
    app.register_blueprint(card_blueprint, url_prefix='')
    app.register_blueprint(folder_blueprint, url_prefix='')
    app.register_blueprint(file_blueprint, url_prefix='')
    app.register_blueprint(LLM_blueprint, url_prefix='')

    return app


if __name__ == '__main__':
    app = create_app()

    app.run()