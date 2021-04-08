type CallbackWorker = (e: MessageEvent) => any;

export default class TextParserWorker{
    private static readonly worker: Worker = new window.Worker('./TextParser.js');
    private static  callbackListener: CallbackWorker|null;

    public static startWorker() {
        this.worker.onerror = (e) => console.log(e);

        this.worker.onmessage = (e) => {
            if (this.callbackListener) {
                this.callbackListener(e);
            }
        };
    }

    public static postMessage(data: any) {
        this.worker.postMessage(data);
    }

    public static terminateWorker() {
        this.worker.terminate()
    }

    public static subscribeWorker(callback: CallbackWorker) {
        this.callbackListener = callback;
    }

    public static unsubscribeWorker(){
        this.callbackListener = null;
    }
}
