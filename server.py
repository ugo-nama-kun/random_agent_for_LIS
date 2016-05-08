# -*- coding: utf-8 -*-

import cherrypy
import argparse
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from random_agent import RandomAgent
import msgpack
import io
from PIL import Image
from PIL import ImageOps
import threading
import numpy as np

parser = argparse.ArgumentParser(description='ml-agent-for-unity')
parser.add_argument('--port', '-p', default='8765', type=int,
                    help='websocket port')
parser.add_argument('--ip', '-i', default='127.0.0.1',
                    help='server ip')
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
args = parser.parse_args()


class Root(object):
    @cherrypy.expose
    def index(self):
        return 'some HTML with a websocket javascript connection'

    @cherrypy.expose
    def ws(self):
        # you can access the class instance through
        handler = cherrypy.request.ws_handler


class AgentServer(WebSocket):
    agent = RandomAgent()
    agent_initialized = False
    cycle_counter = 0
    thread_event = threading.Event()
    log_file = 'reward.log'
    reward_sum = 0
    depth_image_dim = 32 * 32

    def received_message(self, m):
        payload = m.data

        dat = msgpack.unpackb(payload)
        image = Image.open(io.BytesIO(bytearray(dat['image'])))
        depth = Image.open(io.BytesIO(bytearray(dat['depth'])))
        # depth.save("depth_" + str(self.cycle_counter) + ".png")
        # image.save("image_" + str(self.cycle_counter) + ".png")

        depth = np.array(ImageOps.grayscale(depth)).reshape(self.depth_image_dim)

        observation = {"image": image, "depth": depth}
        reward = dat['reward']
        end_episode = dat['endEpisode']

        if not self.agent_initialized:
            self.agent_initialized = True
            print ("initializing agent...")
            self.agent.agent_init(
                use_gpu=args.gpu,
                depth_image_dim=self.depth_image_dim)

            action = self.agent.agent_start(observation)
            self.send(str(action))
            with open(self.log_file, 'w') as the_file:
                the_file.write('cycle, episode_reward_sum \n')
        else:
            self.thread_event.wait()
            self.cycle_counter += 1
            self.reward_sum += reward

            if end_episode:
                action = self.agent.agent_start(observation)  # TODO
                self.send(str(action))
                with open(self.log_file, 'a') as the_file:
                    the_file.write(str(self.cycle_counter) +
                                   ',' + str(self.reward_sum) + '\n')
                self.reward_sum = 0
            else:
                action = self.agent.agent_step(reward, observation)
                self.send(str(action))

        self.thread_event.set()

cherrypy.config.update({'server.socket_port': args.port})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()
cherrypy.config.update({'engine.autoreload.on': False})
config = {'/ws': {'tools.websocket.on': True,
                  'tools.websocket.handler_cls': AgentServer}}
cherrypy.quickstart(Root(), '/', config)
