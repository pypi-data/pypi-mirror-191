from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Bool, validate, TraitError, List, directional_link
import ipywidgets as widgets
from IPython.display import HTML, Javascript, display
from ._frontend import module_name, module_version

import types
from copy import deepcopy
from inspect import isclass, getfullargspec
import json
import esprima
from bs4 import BeautifulSoup

# cannot send multiple msgs in a single function call


@register
class EasyVisWidget(DOMWidget, ValueWidget):
    _model_name = Unicode('EmailModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('EmailView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('example2@example.com').tag(sync=True)

    class States():
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance

        def __setattr__(self, key, value):
            super().__setattr__(key, value)

            if key != 'outer_instance':
                self.outer_instance.update_map_console_html(key, value, 'state')

    mapstate = []

    class Methods():
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance

        def __setattr__(self, key, value):
            super().__setattr__(key, value)

            if key != 'outer_instance':
                self.outer_instance.update_map_console_html(key, value, 'method')

    mapmethod = []

    mounted = False
    cache = []

    output = widgets.Output()  # display area for print()
    map_console_html = Unicode("""
            The following variables and functions are mapped between JS and Python.
            <table>
                <tr>
                    <th>Name</th><th>Kind</th><th>Value</th>
                </tr> 
            </table>  
            <style>table, th, td {
                border:1px solid black;
                padding: 2px 5px;
            }</style>     
        """, sync=True)

    event_console_html = Unicode("""
            Event log in reverse chronological order.
            <div id='event-console'></div>
            <style>
                span.msg_type {
                    padding-right: 10px;
                    color: #f00;
                }
                div#event-console {
                    max-height: 500px;
                    overflow-y: scroll;
                }
                div.msg {
                    line-height: 16px;
                }
            </style>
        """, sync = True)

    def __init__(self, *pargs, **kwargs):
        super(EasyVisWidget, self).__init__(*pargs, **kwargs)

        # display area
        self.init_display()

        self.state = self.createState()
        self.methods = self.createMethod()

        # register on_msg func
        self.on_msg(self.handle_custom_msg)

    def createState(self):
        """factory function for creating the state instance 
        """
        return EasyVisWidget.States(self)

    def createMethod(self):
        """factory function for creating the method instance 
        """
        return EasyVisWidget.Methods(self)

    def init_display(self):
        mapping = widgets.HTML(value="")
        directional_link((self, "map_console_html"), (mapping, "value"))

        event = widgets.HTML(value="")
        directional_link((self, "event_console_html"), (event, "value"))

        console = widgets.Tab()
        console.children = [mapping, event]
        console.titles = ['Map', 'Event']
        console_wrapper = widgets.VBox(
            children=[widgets.Accordion(children=[console], titles=('Console', ''))])

        self.assembly = widgets.VBox(
            children=[self, console_wrapper, self.output])

    def display(self, console=True):
        if console:
            display(self.assembly)
        else:
            display(self)

    def on_rendered(self):
        # init mapstate and mapmethod upon rendered
        self.init_mapstate()
        self.init_mapmethod()

        # execute commands in cache
        for command in self.cache:
            self.js(command)

    def init_mapmethod(self):
        msgs = []

        def make_func(m):
            """
            A helper function for making custom msg funcs

            Args:
                m (str): the method name
            """
            def _function(*pargs):
                self.send(['method', m, pargs])
            return _function

        for m in self.mapmethod:
            if type(m) is dict:
                # the method is defined in py
                keys = list(m.keys())
                if len(keys) != 1:
                    raise Exception(
                        'A mapmethod must be defined as str or dict.')
                key = keys[0]
                setattr(self.methods, key, m[key])
                msgs.append(['py', key])
            elif type(m) is str:
                # the method is expected to be found in js
                setattr(self.methods, m, make_func(m))
                msgs.append(['js', m])
            else:
                raise Exception('A mapmethod must be defined as str or dict.')
        self.send(['mapmethod', msgs])

    def init_mapstate(self):
        msgs = []
        for m in self.mapstate:
            if type(m) is dict:
                keys = list(m.keys())
                if len(keys) != 1:
                    raise Exception(
                        'A mapstate must be defined as str or dict.')
                key = keys[0]
                setattr(self.state, key, m[key])
                msgs.append(['py', key, m[key]])
            elif type(m) is str:
                setattr(self.state, m, None)
                msgs.append(['js', m])
            else:
                raise Exception('A mapstate must be defined as str or dict.')
        self.send(['mapstate', msgs])

    def js(self, jscode: str, **kwargs):
        """Run plain JS
        """
        self.send(['js', jscode])

    def js_init(self, jscode, **kwargs):
        # split kwargs into values and methods
        methods = []
        for key, value in list(kwargs.items()):
            if isinstance(value, types.FunctionType):
                # if pass a py func, wrap it as a method
                del kwargs[key]
                methods.append(key)
                setattr(self.methods, key, value)
            elif isclass(value):
                raise Exception('Cannot pass a class object to js.')
            else:
                pass

        # static analysis to find JS declarations
        js_declaration_vnames = []
        try:
            js_declarations = parseJS(jscode)
            js_declaration_vnames = [v.name for v in js_declarations]
        except:
            pass

        msg = ['script', jscode, kwargs, methods, js_declaration_vnames]
        self.send(msg)

    def register_state(self, property, value):
        """May not need"""
        self.send_js_code("element.{} = {}".format(property, value))
        setattr(self.state, property, value)
        # self.state[property] = value

    def send_js_code(self, jscode):
        """May not need"""
        self.send(['script', jscode])

    def send(self, msg):
        super().send(msg)

        self.update_event_console_html(msg)

    def update_event_console_html(self, msg):
        msg_type, *args = msg

        soup = BeautifulSoup(self.event_console_html, features="html.parser")

        wrapper = soup.new_tag('div', attrs={"class": "msg"})
        msg_type_span = soup.new_tag('span', attrs={"class": "msg_type {}".format(msg_type)} )
        msg_type_span.string = msg_type_to_print(msg_type)
        args_span = soup.new_tag('span', attrs={"class": "args"} )
        args = str(args)
        if len(args) > 40:
            args = args[:40] + " ... (Too large to display)"
        args_span.string = args

        wrapper.append(msg_type_span)
        wrapper.append(args_span)

        # soup.find('div', id='event-console').append(wrapper)
        soup.find('div', id='event-console').insert(0, wrapper)

        self.event_console_html = str(soup)

    def update_map_console_html(self, key: str, value, kind: str):
        soup = BeautifulSoup(self.map_console_html, features="html.parser")
        try_find_tr = soup.find('tr', id=key)
        if try_find_tr:
            if kind == 'method':
                return
            try_find_td_value = try_find_tr.find('td', class_='value')
            try_find_td_value.string = value_to_str(value, kind)
        else:
            tr = soup.new_tag('tr', id=key)
            if kind == 'state':
                _from = 'py' if value else 'js'
            elif kind == 'method':
                _from = 'js' if 'EasyVisWidget.init_mapmethod' in str(value) else 'py'
            
            _from += ' {}'.format(kind)

            td_name = soup.new_tag('td', attrs={"class": "name"})
            td_name.string = key
            td_from = soup.new_tag('td', attrs={"class": "from"})
            td_from.string = _from
            td_value = soup.new_tag('td', attrs={"class": "value"})
            td_value.string = value_to_str(value, kind)

            tr.append(td_name)
            tr.append(td_from)
            tr.append(td_value)

            table = soup.find('table')
            table.append(tr)

        self.map_console_html = str(soup)

    def __getitem__(self, key):
        return getattr(self, key)

    def handle_custom_msg(self, widget, content, buffers):
        """Handle custom msg from JS"""
        output = self.output
        msg_type = content['type']

        if output is not None:
            with output:
                if msg_type == 'error':
                    print('Error msg in JS:', content['content'])
                elif msg_type == 'syncState':
                    pass
                    # temp_obj = deepcopy(content)
                    # if len(json.dumps(content['state'])) > 100:
                    #     del temp_obj['state']
                    # print('sync', temp_obj)
                else:
                    pass

        if content['type'] == 'callback':
            # if JS calls a py method, execute it with args
            method = content['method']
            args = content['args']
            func = getattr(self.methods, method)
            func(*args)
        elif content['type'] == 'rendered':
            # On rendered
            self.on_rendered()
        elif content['type'] == 'syncState':
            # Sync state event
            state = content['state']
            self.sync_state(state)

            self.update_event_console_html(['Sync state', state])
        elif content['type'] == 'error':
            self.update_event_console_html(['JS Error', content['content']])

    def sync_state(self, state):
        for key, value in state.items():
            setattr(self.state, key, value)

    def add_bug_msg(self, msg):
        print(msg)

    def import_es6(self, import_command: str, import_name: str):
        """A hard-coded way to import es6 JS modules.
        Ref: https://github.com/dotnet/interactive/issues/1993

        Args:
            import_command (str): e.g., "import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm"
            import_name (str): the module name, e.g., d3
        """
        display(HTML("""
            <script type="module">
                {0}
                window.{1} = {1};
            </script>
        """.format(import_command, import_name)))

    def import_umd(self, js_code, name):
        command = """
            var script = document.createElement('script');
            var url = "{0}"

            script.onload = function () {{
                window.{1} = {1};
            }};
            script.src = url;
            document.head.appendChild(script); 
        """.format(js_code, name)

        self.cache.append(command)


class JSDeclaration():
    """
    The JS Declaration Class

    Args:
        kind: const | var | let
        name: variable name
        type: CallExpression | ArrowFunctionExpression | ...
        code: raw code for the declaration 
        loc: [start, end]. loc in the entire js code
    """

    def __init__(self, kind, name, type, code, loc):
        self.kind = kind
        self.name = name
        self.type = type
        self.code = code
        self.loc = loc

    def __str__(self):
        return self.code


def parseJS(js_code: str):
    """_summary_

    Args:
        js_code (str): JS Code

    Returns:
        List[JSDeclaration]: A list of JSDeclaration objects
    """
    variable_declared = []

    for x in esprima.parseScript(js_code, loc=True, range=True).body:
        if x.type == 'VariableDeclaration':
            # get the type in [const, var, let]
            kind = x.kind

            # get the raw code
            start, end = x.range
            c = js_code[start: end]
            loc = x.loc.start.line

            # parse the code to get variables
            for d in x.declarations:
                if d.id.type == 'Identifier':
                    _type = d.init.type if d.init else 'Unknown'
                    v = JSDeclaration(kind, d.id.name, _type, c, loc)
                    variable_declared.append(v)
                elif d.id.type == 'ObjectPattern':
                    # object deconstruct pattern, e.g., let {a} = b. The type of a is unknown
                    for o in d.id.properties:
                        v = JSDeclaration(kind, o.key.name, 'Unknown', c, loc)
                        variable_declared.append(v)
                else:
                    try:
                        v = JSDeclaration(kind, d.id.name, d.init.type, c, loc)
                        variable_declared.append(v)
                    except:
                        print('error parsing {}'.format(d))

    return variable_declared


def value_to_str(value, kind):
    v = ""
    if kind == 'state':
        v = str(value)
        if len(v) < 50:
            return v
        else:
            return 'Too large to display'
    elif kind == 'method':
        # args = getfullargspec(value)[0]
        return str(value)

def msg_type_to_print(msg):
    if msg == 'mapstate':
        return 'Initialize map state'
    elif msg == 'mapmethod':
        return 'Initialize map method'
    elif msg == 'script':
        return 'JavaScript'
    else:
        return msg