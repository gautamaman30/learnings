var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var Dialog = /** @class */ (function () {
    function Dialog() {
    }
    return Dialog;
}());
var WindowsButton = /** @class */ (function () {
    function WindowsButton() {
    }
    WindowsButton.prototype.render = function () {
        console.log("Windows button rendered");
    };
    WindowsButton.prototype.onClick = function (windowsClickHandler) {
        console.log("On click called for windows");
        windowsClickHandler();
    };
    return WindowsButton;
}());
var WebButton = /** @class */ (function () {
    function WebButton() {
    }
    WebButton.prototype.render = function () {
        console.log("Web button rendered");
    };
    WebButton.prototype.onClick = function (webClickHandler) {
        console.log("On click called for web");
        webClickHandler();
    };
    return WebButton;
}());
var WindowsDialog = /** @class */ (function (_super) {
    __extends(WindowsDialog, _super);
    function WindowsDialog() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WindowsDialog.prototype.createButton = function () {
        return new WindowsButton();
    };
    return WindowsDialog;
}(Dialog));
var WebDialog = /** @class */ (function (_super) {
    __extends(WebDialog, _super);
    function WebDialog() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WebDialog.prototype.createButton = function () {
        return new WebButton();
    };
    return WebDialog;
}(Dialog));
var App = /** @class */ (function () {
    function App() {
    }
    App.prototype.initialize = function (platform) {
        if (platform === "windows") {
            this.dialog = new WindowsDialog();
        }
        else if (platform === "web") {
            this.dialog = new WebDialog();
        }
        else {
            throw new Error("Platform not supported");
        }
    };
    App.prototype.main = function () {
        this.initialize("windows");
    };
    return App;
}());
var app = new App();
app.main();
