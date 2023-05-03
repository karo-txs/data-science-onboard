from infra.data.pgsql.repository.movie_repository import MovieRepository
from application.services.movie_app_service import MovieAppService
from infra.data.pgsql.context.pgsql_context import PgsqlContext
from infra.data.pgsql.db_connection import DbConnection
import dependency_injector.containers as containers
import dependency_injector.providers as providers
import logging.config
import configparser
import logging
import os


class FlaskDependencyInjectorBootStrapper(containers.DeclarativeContainer):

    # App Config
    #database_config = configparser.ConfigParser(os.environ)
    #database_config.read("./services/api/configurations/database.ini")
    #logging.config.fileConfig("infra/cross_cutting/logging/logging.conf")

    database_config = {
        "postgresql":{
            "database": "postgres",
            "host": "localhost",
            "user": "postgres",
            "password": "postgres",
            "port" : "5433"
            }
    }

    # Infra - Data
    db_connection = DbConnection(
        dbname=database_config["postgresql"].get("database"),
        host=database_config["postgresql"].get("host"),
        user=database_config["postgresql"].get("user"),
        password=database_config["postgresql"].get("password"),
        port=database_config["postgresql"].get("port"),
    )
    context = providers.Singleton(PgsqlContext, db_connection=db_connection)

    movie_repository = providers.Singleton(MovieRepository, context=context)

    # Application Services
    app_service = providers.Singleton(
        MovieAppService, movie_repository=movie_repository
    )
