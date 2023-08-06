/* tslint:disable:no-unused-variable */

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';
import onChange from 'on-change';
import $ from 'jquery';

// window.$ = $;

// Import the CSS
import '../css/widget.css';

declare global {
  interface HTMLElement {
    state: any;
    methods: any;
    pyCallbacks: any;
    methodsToMatch: string[];
    stateToMatch: string[];
  }
  interface Window {
    $: any;
  }
}

type MapStates = string[];
type MapMethods = string[];
type PyKwargs = { [key: string]: any };
type CallBacks = string[];

type MapMethodMsg = ['js' | 'py', string];
type MapStateMsg = ['js' | 'py', string, any?];

export class EmailModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: EmailModel.model_name,
      _model_module: EmailModel.model_module,
      _model_module_version: EmailModel.model_module_version,
      _view_name: EmailModel.view_name,
      _view_module: EmailModel.view_module,
      _view_module_version: EmailModel.view_module_version,
      value: 'Hello World',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'EmailModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'EmailView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class EmailView extends DOMWidgetView {
  private _emailInput: HTMLInputElement;

  private syncLock: boolean;

  render() {
    const that = this;

    window['$'] = $;

    // override console.log to return args
    // const test = () => {
    //   console.error('test');
    // };
    // const _log = console.log.bind(console);
    // console.log = function (...args) {
    //   _log.apply(this, args);
    // that.send({
    //   type: 'cl',
    //   code: args || '',
    //   content: args || '',
    // });
    // };

    // expose element in the JS scope
    const element = that.el;
    element.state = {};
    element.state = onChange(element.state, that.onStateChange.bind(that));
    element.stateToMatch = [];
    console.log('bind element', element);
    console.log('bind state', element.state);

    element.methods = {};
    element.methodsToMatch = [];

    // py callbacks passed to js
    element.pyCallbacks = {};

    this.model.on('msg:custom', (content: any) => {
      console.log('msg:custom', JSON.parse(JSON.stringify(content)));

      if (!Array.isArray(content)) {
        this.sendErrorMsg('invalid custom msg');
      }

      const msgType = content.shift();

      if (msgType === 'script') {
        const jsCode = content.shift();
        // const mapstates = content[0] as MapStates;
        // const mapmethods = content[1] as MapMethods;
        const pykwargs = content[0] as PyKwargs;
        const callbacks = content[1] as CallBacks;
        const jsDeclarations = content[2] as string[];

        this.handleScriptMsg(jsCode, pykwargs, callbacks, jsDeclarations);
      } else if (msgType === 'method') {
        const [method, kargs] = content;
        this.handleMethodMsg(method, kargs);
      } else if (msgType === 'mapmethod') {
        const mapMethodsMsg = content[0] as MapMethodMsg[];
        this.handleMapMethodMsg(mapMethodsMsg);
      } else if (msgType === 'mapstate') {
        const mapStateMsg = content[0] as any;
        this.handleMapStateMsg(mapStateMsg);
      } else if (msgType === 'js') {
        console.log(content[0]);
        eval(content[0]);
      }

      // else if (msgType === 'get') {
      // if (jsCode in state) {
      //   jsCode = `element.state.${jsCode}`;
      // } else {
      //   throw Error(`Variable ${state} not exists in the scope!`);
      // }
      //   that.evalJSScript(jsCode, 'get_callback');
      // }
    });

    this.sendMsg('rendered');
  }

  _state(): any {
    return this.el.state;
  }

  _methods(): any {
    return this.el.methods;
  }

  onStateChange(path: string, value: any, previousValue: any, applyData: any) {
    if (this.syncLock || value === previousValue) {
      // disable when locked, or the value does not change (shallow compare)
      return;
    }

    const stateParameter = path.split('.')[0];
    const state = this._state();

    console.error('onStateChange', state, stateParameter);

    this.sendMsg('syncState', {
      state: {
        [stateParameter]: state[stateParameter],
      },
    });
    // console.log('onStateChange', stateParameter, value);
  }

  /**
   * Return a JS code for unpacking state
   * @returns
   */
  _mapstate(jsDeclarations: string[]): string {
    const state = this._state();
    let stateProperties = Object.keys(state);
    if (jsDeclarations && jsDeclarations.length) {
      stateProperties = stateProperties.filter(
        (x) => jsDeclarations.includes(x) === false // do not match those who declared in JS code
      );
    }

    const jsCode = stateProperties.length
      ? `try {
        var {${stateProperties.join()}} = state;
      } catch (e) {
      };`
      : '';
    return jsCode;
  }

  _mapmethods(jsDeclarations: string[]): string {
    const method = this._methods();
    let methods = Object.keys(method);
    if (jsDeclarations && jsDeclarations.length) {
      // do not match those who declared in JS code
      methods = methods.filter((x) => jsDeclarations.includes(x) === false);
    }

    const jsCode = methods.length
      ? `try {
        var {${methods.join()}} = element.methods;
      } catch (e) {
      };`
      : '';
    return jsCode;
  }

  handleMethodMsg(method: any, kargs: any) {
    const methods = this._methods();
    if (!(method in methods)) {
      throw Error(`Method ${method} is not found.`);
    }
    methods[method].apply(null, kargs);
  }

  handleScriptMsg(
    jsCode: string,
    pykwargs: PyKwargs,
    callbacks: CallBacks,
    jsDeclarations: string[]
  ) {
    console.log('handleScriptMsg', pykwargs, callbacks, jsDeclarations);
    const that = this;
    const element = this.el;
    const state = this._state();
    const methods = this._methods();

    // disable sync state until finishing eval()
    this.syncLock = true;

    // init pykwargs in js
    let js_prefix = ';';

    // unpack state and method
    const j = this._mapstate(jsDeclarations);
    if (j && j.length) {
      js_prefix += j;
    }
    const m = this._mapmethods(jsDeclarations);
    if (m && m.length) {
      js_prefix += m;
    }

    // register callbacks
    if (callbacks && Object.keys(callbacks).length) {
      for (const callback of callbacks) {
        const cf = `function (...args) { 
          element.pyCallbacks.${callback}.apply(null, args); 
        }`;
        const c = `if (typeof ${callback} === "undefined") {
          var ${callback} = ${cf};
        } else {
          ${callback} = ${cf};
        }`;
        js_prefix += c;
        element.pyCallbacks[callback] = (...args: any[]) => {
          // console.error('onsend', 'callback');
          this.sendMsg('callback', {
            method: callback,
            args: args,
          });
        };
      }
    }

    // register pykwargs
    for (const pykwarg in pykwargs) {
      // let temp_value = value
      const c = `if (typeof ${pykwarg} === 'undefined') {
        var ${pykwarg} = pykwargs.${pykwarg};
      } else {
        ${pykwarg} = pykwargs.${pykwarg};
      };`;
      js_prefix += c;
    }

    // register and update states
    let js_postfix = ';';
    for (const mapstate of Object.keys(state)) {
      js_postfix += `state.${mapstate} = ${mapstate};`;
    }
    for (const m of element.stateToMatch) {
      js_postfix += `try {
        state.${m} = ${m};
        element.stateToMatch = element.stateToMatch.filter(x => x != ${m});
      } catch (e) {}`;
    }

    for (const mapmethod of Object.keys(methods)) {
      js_postfix += `element.methods.${mapmethod} = ${mapmethod};`;
    }
    for (const m of element.methodsToMatch) {
      js_postfix += `try {
        element.methods.${m} = ${m};
        element.methodsToMatch = element.methodsToMatch.filter(x => x != ${m});
      } catch (e) {
        console.error("fail to map method", e);
      }`;
    }

    // execute js code
    jsCode = js_prefix + jsCode + js_postfix;
    console.log(jsCode);
    try {
      eval(jsCode);
    } catch (e: unknown) {
      if (e instanceof Error) {
        console.error(e.message);
        that.sendErrorMsg(e.message);
      }
    }

    this.syncLock = false;
    this.syncState();
  }

  /**
   * Sync state from JS to py
   */
  syncState() {
    this.sendMsg('syncState', {
      state: this._state(),
    });
  }

  handleMapStateMsg(mapStateMsgs: MapStateMsg[]) {
    const state = this._state();
    const element = this.el;
    let jsCode = '';
    let buffer = {} as any;
    for (const msg of mapStateMsgs) {
      const t = msg.shift();
      if (t === 'js') {
        element.stateToMatch.push(msg[0]);
      } else if (t === 'py') {
        buffer[msg[0]] = msg[1];
        jsCode += `state.${msg[0]} = buffer["${msg[0]}"];`;
      }
    }
    eval(jsCode);
  }

  handleMapMethodMsg(mapMethodsMsgs: MapMethodMsg[]) {
    const methods = this._methods();
    const element = this.el;

    let jsCode = '';
    for (const method of mapMethodsMsgs) {
      const [t, callback] = method;

      if (t === 'js') {
        element.methodsToMatch.push(callback);
        // jsCode += `methods.${callback} = null;`;
      } else if (t === 'py') {
        const cf = `function (...args) { 
          element.methods.${callback}.apply(null, args); 
        }`;
        const c = `if (typeof ${callback} === "undefined") {
          var ${callback} = ${cf};
        } else {
          ${callback} = ${cf};
        }`;
        jsCode += c;
        methods[callback] = (...args: any[]) => {
          // console.error('onsend', 'callback');
          this.sendMsg('callback', {
            method: callback,
            args: args,
          });
        };
      } else {
        this.sendErrorMsg('Invalid mapmethod msg.');
      }
    }

    this.evalJS(jsCode);
  }

  evalJS(jsCode: string) {
    const that = this;
    const methods = this._methods();
    const element = this.$el;
    const state = this._state();
    try {
      eval(jsCode);
    } catch (e: unknown) {
      // console.error(e);
      if (e instanceof Error) {
        console.error(e.message);
        this.sendErrorMsg(e.message);
      }
    }
  }

  // evalJSScript(jsCode: string, type: string) {
  //   const element = this.el;

  //   const state = (element as any).state;
  //   const stateProperties = Object.keys(state);
  //   let t = '';
  //   if (stateProperties.length) {
  //     t = `let {${stateProperties.join()}} = element.state`;
  //     eval(t);
  //   }

  //   const result = eval(`${t}; ${jsCode}`);
  //   // console.error('evalJSScript', jsCode, result);

  //   this.send({
  //     type: type,
  //     code: jsCode,
  //     content: result,
  //   });
  // }

  sendMsg(type: string, content: any = {}) {
    this.send({ type, ...content });
  }

  sendErrorMsg(errorMsg: string) {
    const msg = {
      content: errorMsg,
      type: 'error',
    };
    console.error(msg.content);
    this.send(msg);
  }

  // value_changed() {
  //   this.el.textContent = this.model.get('value');
  // }
}
