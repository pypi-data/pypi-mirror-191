"use strict";
(self["webpackChunkjupyterlab_daisy"] = self["webpackChunkjupyterlab_daisy"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-daisy', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");






// TODO: Should probably split sidebar logic/layout from button class
class ButtonExtension {
    constructor(app, tracker) {
        this.sidebar = undefined;
        this.editor = undefined;
        this.daisy_address = "";
        this.app = app;
        this.tracker = tracker;
    }
    // Closes the sidebar and replaces the selected text
    // TODO: If the user modifies the selection, the sidebar should also close
    closeAndReplace(ev, sidebar) {
        var _a, _b;
        sidebar === null || sidebar === void 0 ? void 0 : sidebar.close();
        let chosen = (_a = ev.target.textContent) !== null && _a !== void 0 ? _a : '';
        (_b = this.editor) === null || _b === void 0 ? void 0 : _b.replaceSelection(`${chosen}`);
    }
    setDaisyAddress(daisy_address) {
        this.daisy_address = daisy_address;
    }
    populateList(asset_name, list) {
        while (list.firstChild != null) {
            list.removeChild(list.firstChild);
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)(`get-joinable?asset_id=${asset_name}`)
            .then(json => {
            json['JoinableTables'].forEach((entry) => {
                const bla = document.createElement('li');
                bla.setAttribute('title', `Matched ${entry.matches.length} columns, click '+' for details...`);
                const button = document.createElement('button');
                button.className = 'my-button';
                button.textContent = '+';
                const text = document.createElement('p');
                text.textContent = entry.table_path.split('/')[0];
                text.className = 'my-list-item-text';
                const tableContainer = document.createElement('div');
                const table = document.createElement('table');
                table.setAttribute('style', 'width: 100%;');
                tableContainer.className =
                    'my-column-table-div-collapsed';
                tableContainer.setAttribute('style', 'height: 0px');
                tableContainer.appendChild(table);
                bla.appendChild(button);
                bla.appendChild(text);
                bla.appendChild(tableContainer);
                bla.className = 'my-list-item';
                const tableHeader = document.createElement('tr');
                tableHeader.innerHTML = `
                    <th>Column Name</th>
                    <th align="right">COMA Score</th>
                    `;
                table.appendChild(tableHeader);
                entry.matches.forEach(match => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${match['PK']['from_id']}</td>
                        <td class='alnright'>${match['RELATED']['coma']}</td>
                      `;
                    table.appendChild(tr);
                });
                button.onclick = () => {
                    if (tableContainer.className === 'my-column-table-div') {
                        tableContainer.className =
                            'my-column-table-div-collapsed';
                        button.className = 'my-button';
                        button.textContent = '+';
                        tableContainer.setAttribute('style', 'height: 0px');
                    }
                    else {
                        tableContainer.className = 'my-column-table-div';
                        button.className = 'my-button-toggled';
                        button.textContent = '-';
                        tableContainer.setAttribute('style', `height: ${table.clientHeight}px`);
                    }
                };
                text.onclick = ev => this.closeAndReplace(ev, this.sidebar);
                list.appendChild(bla);
            });
        })
            .catch(reason => { console.error('AEUHHH????', reason); });
    }
    createNew(panel, context) {
        const mybutton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.paletteIcon,
            tooltip: "Augment Data",
            onClick: () => {
                var _a, _b, _c, _d;
                (_a = this.sidebar) === null || _a === void 0 ? void 0 : _a.close();
                const activeCell = this.tracker.activeCell;
                if (activeCell !== null) {
                    this.editor = activeCell.editor;
                    let value = this.editor.getRange(this.editor.getCursor('start'), this.editor.getCursor('end'));
                    this.sidebar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Panel();
                    this.sidebar.addClass('my-panel');
                    this.sidebar.id = 'daisy-jupyterlab';
                    this.sidebar.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.paletteIcon;
                    this.app.shell.add(this.sidebar, 'right', { rank: 50000 });
                    this.app.shell.activateById(this.sidebar.id);
                    const header = document.createElement('h1');
                    header.textContent = 'Related Datasets';
                    const form = document.createElement('form');
                    const inp = document.createElement('input');
                    inp.type = "text";
                    inp.name = "name";
                    inp.value = value;
                    inp.className = 'my-highlighted-item';
                    const list = document.createElement('ul');
                    list.className = 'my-list';
                    form.appendChild(inp);
                    const temp = this;
                    form.onsubmit = function (event) {
                        event.preventDefault();
                        event.stopPropagation();
                        // TODO: Split off population of bar to other function
                        // populateList(event.)
                        const name = form.elements[0];
                        console.log(name.value);
                        temp.populateList(name.value, list);
                    };
                    (_b = this.sidebar) === null || _b === void 0 ? void 0 : _b.node.appendChild(header);
                    (_c = this.sidebar) === null || _c === void 0 ? void 0 : _c.node.appendChild(form);
                    (_d = this.sidebar) === null || _d === void 0 ? void 0 : _d.node.appendChild(list);
                    this.populateList(value, list);
                }
            }
        });
        // Add the toolbar button to the notebook toolbar
        panel.toolbar.insertItem(10, 'mybutton', mybutton);
        return mybutton;
    }
}
/**
 * Initialization data for the jupyterlab_daisy extension.
 */
const plugin = {
    id: 'jupyterlab_daisy:plugin',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, settingRegistry, palette, tracker) => {
        console.log('JupyterLab extension jupyterlab_daisy is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupyterlab_daisy settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab_daisy.', reason);
            });
        }
        const button = new ButtonExtension(app, tracker);
        app.docRegistry.addWidgetExtension('Notebook', button);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.830d5ec51a23a5285275.js.map