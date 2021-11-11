from invoice_app import create_app

from invoice_app.config import ProdConfig, DevConfig

app = create_app(config_class=ProdConfig)

if __name__ == '__main__':
    app.run(debug=True)