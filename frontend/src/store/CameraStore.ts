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
    update: (camera: Camera) => {
        const index = cameraStoreMutations.getIndex(camera.id as number)
        cameraStoreState.camerasArray[index] = camera
    },
    remove: (id: number) => {
        const removeIndex = cameraStoreState.camerasArray.map((cam) => {
            return cam.id
        }).indexOf(id)
        cameraStoreState.camerasArray.splice(removeIndex, 1)
    },
    get: (id: number) => {
        const index = cameraStoreMutations.getIndex(id)
        return cameraStoreState.camerasArray[index]
    },
    getIndex: (id: number) => {
        return cameraStoreState.camerasArray.indexOf(cameraStoreState.camerasArray.find((e: any) => e.id == id) as Camera)
    },
    getList: async () => {
        const cameraService = new CameraService();
        cameraStoreState.camerasArray = await cameraService.getCameras()
    }
}
