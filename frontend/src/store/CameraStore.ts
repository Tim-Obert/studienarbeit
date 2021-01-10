import Vue from 'vue'
import CameraService from "@/services/CameraService";
import {Camera} from "@/interfaces/CameraInterface";

export const cameraStoreState = Vue.observable({
    camerasArray: new Array<Camera>()
})

export const cameraStoreMutations = {
    add: (camera: Camera) => {
        cameraStoreState.camerasArray.push(camera)
    },
    remove: (name: string) => {
        const removeIndex = cameraStoreState.camerasArray.map((cam) => {
            return cam.name
        }).indexOf(name)
        cameraStoreState.camerasArray.splice(removeIndex, 1)
    },
    getList: async () => {
        const cameraService = new CameraService();
        cameraStoreState.camerasArray = await cameraService.getCameras()
    }
}
