from dotenv import load_dotenv
load_dotenv()

from invoice_app import create_app
from invoice_app.config import DevConfig


app = create_app(config_class=DevConfig())

if __name__ == "__main__":
    app.run(debug=True)
