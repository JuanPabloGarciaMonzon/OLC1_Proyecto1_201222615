from graphviz import Digraph
import os
class grafica():

    def grafoString(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",label="S1")
        dot.node("S2",label="S2")
        dot.node("S2",shape="doublecircle")
        dot.edge("S0", "S1", label="\"")
        dot.edge("S1", "S1", label=".")
        dot.edge("S1", "S1", label="\\S")
        dot.edge("S1", "S2", label="\"")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/String.gv"
        dot.render(direction, view=False)

    def grafoChar(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",label="S1")
        dot.node("S2",label="S2")
        dot.node("S2",shape="doublecircle")
        dot.edge("S0", "S1", label="\'")
        dot.edge("S1", "S1", label=".")
        dot.edge("S1", "S1", label="\\S")
        dot.edge("S1", "S2", label="\'")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/Char.gv"
        dot.render(direction, view=False)

    def grafoNumber(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",shape="doublecircle")
        dot.edge("S0", "S1", label="D")
        dot.edge("S1", "S1", label="D")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/Number.gv"
        dot.render(direction, view=False)

    def grafoID(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",shape="doublecircle")
        dot.edge("S0", "S1", label="ID")
        dot.edge("S1", "S1", label="ID")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/ID.gv"
        dot.render(direction, view=False)

    def grafoDecimal(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",label="S1")
        dot.node("S2",label="S2")
        dot.node("S3",label="S3")
        dot.node("S4",label="S4")
        dot.node("S4",shape="doublecircle")
        dot.edge("S0", "S1", label="D")
        dot.edge("S1", "S2", label="D")
        dot.edge("S2", "S2", label="D")
        dot.edge("S2", "S3", label=".")
        dot.edge("S3", "S4", label="D")
        dot.edge("S4", "S4", label="D")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/Decimal.gv"
        dot.render(direction, view=False)

    def grafoMultiComment(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",label="S1")
        dot.node("S2",label="S2")
        dot.node("S3",label="S3")
        dot.node("S4",label="S4")
        dot.node("S4",shape="doublecircle")
        dot.edge("S0", "S1", label="/")
        dot.edge("S1", "S2", label="*")
        dot.edge("S2", "S2", label=".")
        dot.edge("S2", "S2", label="/S")
        dot.edge("S2", "S3", label="*")
        dot.edge("S3", "S4", label="/")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/MultiComentario.gv"
        dot.render(direction, view=False)

    def grafoUniComment(self):
        count = 0
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')
        dot.node("S0",label="S0")
        dot.node("S1",label="S1")
        dot.node("S2",label="S2")
        dot.node("S3",label="S3")
        dot.node("S3",shape="doublecircle")
        dot.edge("S0", "S1", label="/")
        dot.edge("S1", "S2", label="/")
        dot.edge("S2", "S2", label=".")
        dot.edge("S2", "S3", label="/n")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "/Grafos/UniComentario.gv"
        dot.render(direction, view=False)
