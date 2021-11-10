from invoice_app import create_app
import datetime

app = create_app()

if __name__ == '__main__':
    from dotenv import load_dotenv
    # load_dotenv()
    app.config["SECRET_KEY"] = "super-secret"
    app.config["JWT_SECRET_KEY"] = "kurwajapierdole"
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ['cookies']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=20)
    
    app.run(debug=True)