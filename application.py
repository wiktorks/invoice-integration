from dotenv import load_dotenv
load_dotenv()
from invoice_app import create_app
import os

from invoice_app.config import ProdConfig, DevConfig

application = create_app(config_class=DevConfig)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(debug=True, host="0.0.0.0", port=port)