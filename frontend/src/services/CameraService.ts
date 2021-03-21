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

    async updateCamera(camera: Camera){
        return this.apiService.put("/camera", {camera: camera})
            .then((res) => {
                cameraStoreMutations.update(camera)
                return res;
            })
    }

    async getCameras(): Promise<Array<Camera>> {
        const cameraArray = new Array<Camera>()
        return await this.apiService.get("/cameras")
            .then((responseBody) => {
                responseBody.map((cam: Camera)=>{
                    cameraArray.push(new Camera(cam.id, cam.name, cam.url, cam.last_motion))
                })
                return cameraArray
            }).catch(() => {
                //alert("No connection to backend")
                return cameraArray
            })
    }

}
