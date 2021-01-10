export default class ApiService {
    get(){
        return 1
    }

    async post(path: string, body? : object){
        return fetch(process.env.VUE_APP_BASE_URL + path, {
            method: "POST",
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                body
            )
        })
    }

    put(){
        return 1
    }

    delete(path: string, body? : object){
        return fetch(process.env.VUE_APP_BASE_URL + path, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                body
            )
        })
    }
}
