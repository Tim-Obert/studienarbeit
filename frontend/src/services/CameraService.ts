import {Camera} from "@/interfaces/CameraInterface"
import ApiService from "@/services/ApiService"

export default class CameraService {
    apiService = new ApiService()

    async addCamera(camera: Camera) {
        return this.apiService.post("/camera", camera)
            .then((res) => {
                //TODO: build store for cameras list and trigger/add-mutation rebuild here
                return res;
        })
    }

    async removeCamera(name: string) {
        return this.apiService.delete("/camera", {name: name})
            .then((res) => {
                return res;
        })
    }
}
