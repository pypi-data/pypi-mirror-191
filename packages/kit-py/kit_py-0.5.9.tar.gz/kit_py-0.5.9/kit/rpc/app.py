# -*- coding: utf-8 -*-
import time

from .job import JobMixin
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .state import State


class ServerMixin:

    def _heartbeat(self, request):
        return JSONResponse({"hello": "job center"})

    def creat_app(self):
        self.server_app = FastAPI(docs_url=None, redoc_url=None)
        self.server_app.add_route("/heartbeat", self._heartbeat, methods=["GET"])
        return self.server_app

    def run(self, *args, **kwargs):
        import uvicorn
        uvicorn.run(self.server_app, *args, **kwargs)


class Rpc(JobMixin, ServerMixin):

    def __init__(self):
        self.app = self.creat_app()
        self.state = State()

    def run_forever(self):
        while True:
            time.sleep(1)


rpc = Rpc()
