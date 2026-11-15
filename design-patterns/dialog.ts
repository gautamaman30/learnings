interface Button {
    render(): void 
    onClick(clickHandler: () => void): void
}

abstract class Dialog {
    abstract createButton(): Button

    render(): void {
        console.log("Calling create button implementation of the platform")
        const okButton = this.createButton()
        okButton.onClick(() => {
            console.log("Dialog logic: Closing the dialog now.")
        })
        okButton.render()
    }
}

class WindowsButton implements Button {
    render() {
        console.log("Windows button rendered")
    }

    onClick(windowsClickHandler: () => void) {
        console.log("On click called for windows")
        windowsClickHandler()
    }
}


class WebButton implements Button {
    render() {
        console.log("Web button rendered")
    }

    onClick(webClickHandler: () => void) {
        console.log("On click called for web")
        webClickHandler()
    }
}

class WindowsDialog extends Dialog {
    createButton() {
        console.log("Windows dialog create button called")
        return new WindowsButton()
    }
}


class WebDialog extends Dialog {
    createButton() {
        console.log("Web dialog create button called")
        return new WebButton()
    }
}

class App {
    private dialog!: Dialog

    initialize(platform: string) {
        if (platform === "windows") {
            this.dialog = new WindowsDialog()
        } else if (platform === "web") {
            this.dialog = new WebDialog()
        } else {
            throw new Error("Platform not supported")
        }
    }

    main() {
        this.initialize("web")
        this.dialog.render()
    }
}

const app = new App()
app.main()

