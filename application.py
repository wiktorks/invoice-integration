from dotenv import load_dotenv
load_dotenv()
from invoice_app import celery
from invoice_app.app_factory import create_app
from invoice_app.config import ProdConfig, DevConfig
import os



if __name__ == '__main__':
    application = create_app(config_class=DevConfig, celery=celery)
    port = int(os.environ.get('PORT', 5000))
    application.run(host="0.0.0.0", port=port, debug=True)