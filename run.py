from invoice_app import create_app
from invoice_app.config import ProdConfig

application = create_app(config_class=ProdConfig)

if __name__ == '__main__':
    application.run()