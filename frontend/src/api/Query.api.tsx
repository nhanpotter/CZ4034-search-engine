import BaseAPI, {methodType} from "./Base.api";

export default class QueryAPI extends BaseAPI{
    public static listRestaurants(callback: any){
        this.JSONRequest('/list', methodType.get, {}, {}, {})
            .then((res: any) => {
                if (callback) {
                    callback({
                        data: res.data,
                        status: 1,
                    })
                }
            })
            .catch(err =>{
                console.log(err)
                if (callback) {
                    callback({
                        status: 0,
                        data: [],
                    })
                }
            })
    }

    public static query(term: string, restaurants: number[], sentiments: number[], queryCounter: number, callback: any) {
        const content = {
            "query": term,
            "res_ids": restaurants,
            "sentiments": sentiments,
        }

        this.JSONRequest('/query', methodType.post, {}, {}, content)
            .then((res: any) => {
                if (callback) {
                    callback({
                        data: res.data.hits.hits,
                        counter: queryCounter,
                        status: 1,
                        time: res.data.took,
                        suggesters: res.suggest.suggest['review-suggestion'][0].options
                    })
                }
            })
            .catch(err =>{
                console.log(err)
                if (callback) {
                    callback({
                        status: 0,
                        counter: queryCounter,
                        data: [],
                        time: 0
                    })
                }
            })
    }

    public static crawl(url: string, count: number, callback: any){
        const content = {
            url: url,
            count: count
        }

        this.JSONRequest('/add', methodType.post, {}, {}, content)
            .then((res: any) => {
                if (callback) {
                    callback({
                        data: res,
                        status: 1,
                    })
                }
            })
            .catch(err =>{
                console.log(err)
                if (callback) {
                    callback({
                        status: 0,
                        data: {},
                    })
                }
            })
    }

    public static classify(text: string, callback: any){
        const constent = {
            text: text
        }

        this.JSONRequest('/classify', methodType.post, {}, {}, constent)
            .then((res: any) => {
                if (callback) {
                    callback({
                        data: res.data,
                        status: 1,
                    })
                }
            })
            .catch(err =>{
                console.log(err)
                if (callback) {
                    callback({
                        status: 0,
                        data: [],
                    })
                }
            })
    }
}
