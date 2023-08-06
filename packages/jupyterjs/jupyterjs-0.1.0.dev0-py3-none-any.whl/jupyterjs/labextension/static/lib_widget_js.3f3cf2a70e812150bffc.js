(self["webpackChunkjupyterjs"] = self["webpackChunkjupyterjs"] || []).push([["lib_widget_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) AY
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/* tslint:disable:no-unused-variable */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.EmailView = exports.EmailModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const on_change_1 = __importDefault(__webpack_require__(/*! on-change */ "webpack/sharing/consume/default/on-change/on-change"));
const jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"));
// window.$ = $;
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class EmailModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: EmailModel.model_name, _model_module: EmailModel.model_module, _model_module_version: EmailModel.model_module_version, _view_name: EmailModel.view_name, _view_module: EmailModel.view_module, _view_module_version: EmailModel.view_module_version, value: 'Hello World' });
    }
}
exports.EmailModel = EmailModel;
EmailModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
EmailModel.model_name = 'EmailModel';
EmailModel.model_module = version_1.MODULE_NAME;
EmailModel.model_module_version = version_1.MODULE_VERSION;
EmailModel.view_name = 'EmailView'; // Set to null if no view
EmailModel.view_module = version_1.MODULE_NAME; // Set to null if no view
EmailModel.view_module_version = version_1.MODULE_VERSION;
class EmailView extends base_1.DOMWidgetView {
    render() {
        const that = this;
        window['$'] = jquery_1.default;
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
        element.state = on_change_1.default(element.state, that.onStateChange.bind(that));
        element.stateToMatch = [];
        console.log('bind element', element);
        console.log('bind state', element.state);
        element.methods = {};
        element.methodsToMatch = [];
        // py callbacks passed to js
        element.pyCallbacks = {};
        this.model.on('msg:custom', (content) => {
            console.log('msg:custom', JSON.parse(JSON.stringify(content)));
            if (!Array.isArray(content)) {
                this.sendErrorMsg('invalid custom msg');
            }
            const msgType = content.shift();
            if (msgType === 'script') {
                const jsCode = content.shift();
                // const mapstates = content[0] as MapStates;
                // const mapmethods = content[1] as MapMethods;
                const pykwargs = content[0];
                const callbacks = content[1];
                const jsDeclarations = content[2];
                this.handleScriptMsg(jsCode, pykwargs, callbacks, jsDeclarations);
            }
            else if (msgType === 'method') {
                const [method, kargs] = content;
                this.handleMethodMsg(method, kargs);
            }
            else if (msgType === 'mapmethod') {
                const mapMethodsMsg = content[0];
                this.handleMapMethodMsg(mapMethodsMsg);
            }
            else if (msgType === 'mapstate') {
                const mapStateMsg = content[0];
                this.handleMapStateMsg(mapStateMsg);
            }
            else if (msgType === 'js') {
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
    _state() {
        return this.el.state;
    }
    _methods() {
        return this.el.methods;
    }
    onStateChange(path, value, previousValue, applyData) {
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
    _mapstate(jsDeclarations) {
        const state = this._state();
        let stateProperties = Object.keys(state);
        if (jsDeclarations && jsDeclarations.length) {
            stateProperties = stateProperties.filter((x) => jsDeclarations.includes(x) === false // do not match those who declared in JS code
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
    _mapmethods(jsDeclarations) {
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
    handleMethodMsg(method, kargs) {
        const methods = this._methods();
        if (!(method in methods)) {
            throw Error(`Method ${method} is not found.`);
        }
        methods[method].apply(null, kargs);
    }
    handleScriptMsg(jsCode, pykwargs, callbacks, jsDeclarations) {
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
                element.pyCallbacks[callback] = (...args) => {
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
        }
        catch (e) {
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
    handleMapStateMsg(mapStateMsgs) {
        const state = this._state();
        const element = this.el;
        let jsCode = '';
        let buffer = {};
        for (const msg of mapStateMsgs) {
            const t = msg.shift();
            if (t === 'js') {
                element.stateToMatch.push(msg[0]);
            }
            else if (t === 'py') {
                buffer[msg[0]] = msg[1];
                jsCode += `state.${msg[0]} = buffer["${msg[0]}"];`;
            }
        }
        eval(jsCode);
    }
    handleMapMethodMsg(mapMethodsMsgs) {
        const methods = this._methods();
        const element = this.el;
        let jsCode = '';
        for (const method of mapMethodsMsgs) {
            const [t, callback] = method;
            if (t === 'js') {
                element.methodsToMatch.push(callback);
                // jsCode += `methods.${callback} = null;`;
            }
            else if (t === 'py') {
                const cf = `function (...args) { 
          element.methods.${callback}.apply(null, args); 
        }`;
                const c = `if (typeof ${callback} === "undefined") {
          var ${callback} = ${cf};
        } else {
          ${callback} = ${cf};
        }`;
                jsCode += c;
                methods[callback] = (...args) => {
                    // console.error('onsend', 'callback');
                    this.sendMsg('callback', {
                        method: callback,
                        args: args,
                    });
                };
            }
            else {
                this.sendErrorMsg('Invalid mapmethod msg.');
            }
        }
        this.evalJS(jsCode);
    }
    evalJS(jsCode) {
        const that = this;
        const methods = this._methods();
        const element = this.$el;
        const state = this._state();
        try {
            eval(jsCode);
        }
        catch (e) {
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
    sendMsg(type, content = {}) {
        this.send(Object.assign({ type }, content));
    }
    sendErrorMsg(errorMsg) {
        const msg = {
            content: errorMsg,
            type: 'error',
        };
        console.error(msg.content);
        this.send(msg);
    }
}
exports.EmailView = EmailView;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"jupyterjs","version":"0.1.0","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/myorg/jupyterjs","bugs":{"url":"https://github.com/myorg/jupyterjs/issues"},"license":"BSD-3-Clause","author":{"name":"AY","email":"me@me.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/myorg/jupyterjs"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf jupyterjs/labextension","clean:nbextension":"rimraf jupyterjs/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","on-change":"^4.0.2"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"jupyterjs/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.3f3cf2a70e812150bffc.js.map