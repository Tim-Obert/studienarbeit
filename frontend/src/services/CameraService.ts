import {Camera} from "@/interfaces/CameraInterface"
import ApiService from "@/services/ApiService"
import {cameraStoreMutations} from "@/store/CameraStore";

export default class CameraService {
    apiService = new ApiService()

    async addCamera(camera: Camera) {
        return this.apiService.post("/camera", camera)
            .then((res) => {
                cameraStoreMutations.add(camera)
                return res;
        })
    }

    async removeCamera(name: string) {
        return this.apiService.delete("/camera", {name: name})
            .then((res) => {
                cameraStoreMutations.remove(name)
                return res;
        })
    }

    async updateCamera(){
        //TODO: Implement, if cameras are identified via id
        return 1
    }

    async getCameras(): Promise<Array<Camera>> {
        return await this.apiService.get("/cameras")
            .then((responseBody) => {
                const cameraArray = new Array<Camera>()
                responseBody.map((cam: Camera)=>{
                    cameraArray.push(cam)
                })
                return cameraArray
            })
    }

}
