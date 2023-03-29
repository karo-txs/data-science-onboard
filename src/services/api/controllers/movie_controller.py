import sys

sys.path.append("../../../../src")

from infra.cross_cutting.ioc.flask_dependency_injector_boot_strapper import (
    FlaskDependencyInjectorBootStrapper as container,
)
from infra.cross_cutting.exceptions.formatters.exception_formatter import (
    ExceptionFormatter as ExFormatter,
)
from services.api.configurations.app_configuration import AppConfiguration
from services.api.auto_mapper.json_to_view_model_mapping import (
    GenericJsonToViewModelMapping as ViewModelMapper,
)
from services.api.data_transfer_objects.success_response_dto import SuccessResponseDto
from services.api.data_transfer_objects.error_response_dto import ErrorResponseDto
from application.view_models.movie_view_model import MovieViewModel
from flask import Flask, request, jsonify
from dataclasses import asdict
import logging
import uuid


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


@app.route(f"/register", methods=["POST"])
def register():
    try:
        code = 200
        json_data = request.get_json()
        logging.info(f"Data received: {json_data}")
        vm = ViewModelMapper.to_view_model(json_data, MovieViewModel)
        result = app_service.register(vm)

        if not result:
            raise Exception(default_error_message)
        else:
            response = asdict(SuccessResponseDto("The movie has been registered."))
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto([str(ex)]))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    logging.info(f"Response: {response}")
    return jsonify(response), code

@app.route(f"/store", methods=["GET"])
def store_movies():
    try:
        code = 200
        result = app_service.store_movies()

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

@app.route(f"/update", methods=["PUT"])
def update():
    try:
        code = 200
        json_data = request.get_json()
        logging.info(f"Data received: {json_data}")
        vm = ViewModelMapper.to_view_model(json_data, MovieViewModel)
        result = app_service.update(vm)
        
        if not result:
            raise Exception(default_error_message)
        else:
            response = asdict(
                SuccessResponseDto(
                    "The movie information has been sent to be updated."
                )
            )
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto([str(ex)]))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    logging.info(f"Response: {response}")
    return jsonify(response), code


@app.route(f"/remove", methods=["DELETE"])
def remove():
    try:
        code = 200
        json_data = request.get_json()
        logging.info(f"Data received: {json_data}")
        result = app_service.remove(uuid.UUID(json_data["id"]))
        if not result:
            raise Exception(default_error_message)
        else:
            response = asdict(SuccessResponseDto("The movie has been deleted."))
        logging.info(response)
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto(str(ex)))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    logging.info(f"Response: {response}")
    return jsonify(response), code


@app.route(f"/get_all", methods=["GET"])
def get_all():
    try:
        code = 200
        customers = app_service.get_all()
        response = {"data": []}
        for customer in customers:
            response["data"].append(asdict(customer))
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto(str(ex)))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    return jsonify(response), code

@app.route(f"/get_by_id", methods=["GET"])
def get_by_id():
    try:
        code = 200
        json_data = request.get_json()
        logging.info(f"Data received: {json_data}")
        customer = app_service.get_by_id(json_data["id"])
        response = {"data": asdict(customer)}
    except Exception as ex:
        code = 500
        response = asdict(ErrorResponseDto(str(ex)))
        ex_formatted = ExFormatter.format(ex)
        logging.error(ex_formatted)
    return jsonify(response), code


if __name__ == "__main__":
    app.run(port=int(api_port), debug=bool(debug), threaded=bool(threaded))
