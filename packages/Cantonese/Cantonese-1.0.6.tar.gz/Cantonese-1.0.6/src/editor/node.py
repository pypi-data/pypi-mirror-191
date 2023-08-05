from node_graphics_node import QDMGraphicsNode
from node_content_widgets import QDMNodeContentWidgets
from node_socket import Socket
from node_socket import LEFT_TOP
from node_socket import LEFT_BOTTOM
from node_socket import RIGHT_TOP
from node_socket import RIGHT_BOTTOM
from node_socket import SOCKET_LOGIC_TYPE
from node_socket import SOCKET_VALUE_TYPE

NODE_FUNC_TYPE = 1
NODE_VARAIBLE_TYPE = 2
NODE_NONE_TYPE = 3
NODE_BRANCH_TYPE = 4
NODE_LOOP_TYPE = 5

TYPE_TO_NAME = {
    1 : 'NODE_FUNC',
    2 : 'NODE_VARAIBLE',
    3 : 'NODE_NONE',
    4 : 'NODE_BRANCH',
    5 : 'NODE_LOOP'
}

class Node():
    def __init__(self, scene, title = "Undefined Node", inputs = [], outputs = [], width = 180, height = 100, 
                    node_type : int = NODE_NONE_TYPE) -> None:
        self.scene = scene
        self.title = title
        self.node_type = node_type
        self.content = QDMNodeContentWidgets()
        # TODO: define different node type's height and width
        self.grNode = QDMGraphicsNode(self, scene, width = 210, height = height)
        self.scene.grScene.addItem(self.grNode)
        self.scene.addNode(self)


        self.socket_spacing = 22

        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            try:
                socket_type = item['type']
            except KeyError:
                # 设置为默认的类型
                socket_type = 1
            try:
                socket_name = item['name']
            except KeyError:
                socket_name = ''
            try:
                value = item['value']
            except KeyError:
                value = ''
            socket = Socket(self, index = counter, position = LEFT_TOP, socket_type = socket_type, socket_name = socket_name, value = value)
            counter += 1
            self.inputs.append(socket)
        counter = 0
        for item in outputs:
            try:
                socket_type = item['type']
            except KeyError:
                # 设置为默认的类型
                socket_type = 1
            try:
                socket_name = item['name']
            except KeyError:
                socket_name = ''
            try:
                value = item['value']
            except KeyError:
                value = ''
            socket = Socket(self, index = counter, position = RIGHT_TOP, socket_type = socket_type, socket_name = socket_name, value = value)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.grNode.width - self.socket_spacing
        
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - \
                self.grNode._padding - index * self.socket_spacing
        else:
            # start form top
            y = self.grNode.title_height + self.grNode._padding \
                + self.grNode.edge_size + index * self.socket_spacing
        return x, y

    def remove(self):
        for socket in (self.inputs + self.outputs):
            if socket.hasEdges():
                for edge in socket.edges:
                    edge.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.scene.removeNode(self)
        self.grNode = None

    def getAllSocketName(self, debug = False):
        
        ret = {}

        # init the return value
        ret['input'] = []
        ret['output'] = []

        for item in self.inputs:
            if debug:
                print(item.socket_id_name)
            ret['input'].append(item.dump())
        for item in self.outputs:
            if debug:
                print(item.socket_id_name)
            ret['output'].append(item.dump())

        return ret

    def findSocketByNameID(self, name):
        for item in self.inputs:
            if name == self.item.socket_id_name:
                return item
        for item in self.outputs:
            if name == self.item.socket_id_name:
                return item


    def getAttr(self):
        self.data = {}
        self.data['node_name'] = self.title
        self.data['node_type'] = TYPE_TO_NAME[self.node_type]
        self.data['socket'] = self.getAllSocketName(debug = False)
        return self.data

    def updateAttr(self, data):
        self.title = data['node_name']
        self.node_type = data['node_type']
        self.inputs = data['socket']['inputs']
        self.outputs = data['socket']['outputs']

    def setTitle(self, t):
        self.title = t
        self.grNode.update()