import sys

sys.path.append("./src")

from api.infra.cross_cutting.ioc.flask_dependency_injector_boot_strapper import (
    FlaskDependencyInjectorBootStrapper as container,
)
from api.infra.cross_cutting.exceptions.formatters.exception_formatter import (
    ExceptionFormatter as ExFormatter,
)
from api.services.api.data_transfer_objects.success_response_dto import SuccessResponseDto
from api.services.api.data_transfer_objects.error_response_dto import ErrorResponseDto
from api.services.api.configurations.app_configuration import AppConfiguration
from flask import Flask, request, jsonify
from dataclasses import asdict
import logging


app = Flask(__name__)
wsgi_app = app.wsgi_app

config = AppConfiguration.configure()

keys = ("flask", )

api_name = config[keys[0]].get("api_name")
api_port = config[keys[0]].get("api_port")
debug = config[keys[0]].get("debug")
threaded = config[keys[0]].get("threaded")

app_service = container.app_service()

default_error_message = "An unknown error has occurred."

@app.route(f"/update_database", methods=["GET"])
def update_database():
    try:
        code = 200
        result = app_service.update_database()

        if not result:
            raise Exception(default_error_message)
        else:
            response = asdict(SuccessResponseDto("New films were stored"))
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto([str(ex)]))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    logging.info(f"Response: {response}")
    return jsonify(response), code

@app.route(f"/train", methods=["GET"])
def train():
    try:
        code = 200
        result = app_service.train()
        response = {"data": result}
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto(str(ex)))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    return jsonify(response), code

@app.route(f"/test", methods=["GET"])
def test():
    try:
        code = 200
        customers = app_service.test()
        response = {"data": []}
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto(str(ex)))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    return jsonify(response), code

@app.route(f"/inference", methods=["GET"])
def inference():
    try:
        code = 200
        response = app_service.get_all()
        response = {"data": response}
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto(str(ex)))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    return jsonify(response), code


if __name__ == "__main__":
    app.run(port=int(api_port), 
            debug=bool(debug), 
            threaded=bool(threaded))
