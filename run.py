from invoice_app import create_app

app = create_app()

if __name__ == '__main__':
    from dotenv import load_dotenv
    # load_dotenv()
    app.config["SECRET_KEY"] = "super-secret"
    app.config["JWT_SECRET_KEY"] = "kurwajapierdole"
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ['cookies']
    app.run(debug=True)