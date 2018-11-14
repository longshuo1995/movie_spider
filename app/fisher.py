from app import create_app, register_blueprint, secure

app = create_app()

register_blueprint(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=secure.debug)
