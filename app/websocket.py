# coding: utf-8

import os
import io
import json
import time

import subprocess

def handle_websocket(ws, path=None):

    print("Websocket type: {}".format(path.split("/")[-1]))
    
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            command = message.split(":")[-1].strip(" ")
            print(command)
            proc = subprocess.Popen(
                [command],
                shell=True,
                stdout=subprocess.PIPE
            )

            for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                print(line)
                ws.send(line)
