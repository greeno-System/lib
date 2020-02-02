from lib.app.equipment.dataInterface.DataInterface import DataInterface
from lib.app.core.application.Application import Application
from lib.app.core.action.Action import Action
from lib.app.core.action.Response import Response as GreenoResponse
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import Response
import json
import _thread

class Web(DataInterface):

    def __init__(self, config = False):
        super().__init__(config)

        self.app = Application.app()

        self.flaskInterface = Flask(__name__)

        self.flaskInterface.add_url_rule(
            '/<module>/<action>',
            'index',
            self.onRequest
        )

    def open(self):

        self.cors = CORS(self.flaskInterface)

        _thread.start_new_thread(self._runFlask, ())

    def _runFlask(self):
        self.flaskInterface.run(
            port=self.config.get("port"), 
            debug=self.app.isDebugMode(),
            use_reloader=False
        )

    def onRequest(self, module, action):
        actionRequest = {}
        actionRequest[Action.REQUEST_MODULE_KEY] = module
        actionRequest[Action.REQUEST_ACTION_KEY] = action
        actionRequest[Action.REQUEST_DATA_KEY] = request.args

        actionResponse = self.request(actionRequest)

        status = actionResponse[Action.RESPONSE_STATUS_KEY]

        if status != GreenoResponse.STATUS_OK:
            return Response(status=status)
        else:
            return Response(json.dumps(actionResponse), status)



    def close(self):
        pass