import os
import configparser


class AppConfiguration:

    @staticmethod
    def configure():
        #app_config = configparser.ConfigParser(os.environ)
        #app_config.read("./services/api/configurations/app_settings.conf")
        return {
            "flask":{
                "api_name":"imdb",
                "api_port":"8008",
                "debug":True,
                "threaded":True
                }
        }
