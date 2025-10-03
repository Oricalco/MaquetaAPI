
#from config import custom_json_serializer
from flask import Flask
#from controllers import estaciones_controller, forecast_controller, mediciones_controller, rem_controller
import os
def create_app():
    app = Flask(__name__)
    #app.json.default = custom_json_serializer
    app.json.ensure_ascii = False
    
    # Registrar blueprints
    #app.register_blueprint(estaciones_controller.bp, url_prefix='/api/itp/estaciones')
    #app.register_blueprint(mediciones_controller.bp, url_prefix='/api/itp/estaciones')
    #app.register_blueprint(forecast_controller.bp, url_prefix='/api/itp/estaciones')
    #app.register_blueprint(rem_controller.bp, url_prefix='/api/itp/rem')
    
    return app


if __name__ == "__main__":
    app = create_app()
    puerto = os.getenv("PUERTO_URI")
    app.run(debug=True, host='0.0.0.0', port=puerto, threaded=True)