import {Camera} from "@/interfaces/CameraInterface"
import ApiService from "@/services/ApiService"
import {cameraStoreMutations} from "@/store/CameraStore";

export default class CameraService {
    apiService = new ApiService()

    async addCamera(camera: Camera) {
        return this.apiService.post("/camera", camera)
            .then(r =>  r.json().then(data => ({status: r.status, body: data})))
            .then((data) => {
                camera.id = data.body.id
                cameraStoreMutations.add(camera)
                return data;
        })
    }

    async removeCamera(id: number) {
        return this.apiService.delete("/camera", {id: id})
            .then((res) => {
                cameraStoreMutations.remove(id)
                return res;
        })
    }

    async updateCamera(){
        //TODO: Implement, if cameras are identified via id
        return 1
    }

    async getCameras(): Promise<Array<Camera>> {
        const cameraArray = new Array<Camera>()
        return await this.apiService.get("/cameras")
            .then((responseBody) => {
                responseBody.map((cam: Camera)=>{
                    cameraArray.push(cam)
                })
                return cameraArray
            }).catch(() => {
                //alert("No connection to backend")
                return cameraArray
            })
    }

}
