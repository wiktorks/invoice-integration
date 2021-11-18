from invoice_app import create_app
from invoice_app.config import ProdConfig, DevConfig
from dotenv import load_dotenv

load_dotenv()
application = create_app(config_class=DevConfig)

if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0")