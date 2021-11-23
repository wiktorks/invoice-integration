from dotenv import load_dotenv
load_dotenv()
from invoice_app import create_app
from invoice_app.config import ProdConfig, DevConfig
import os


application = create_app(config_class=DevConfig)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host="0.0.0.0", port=port)