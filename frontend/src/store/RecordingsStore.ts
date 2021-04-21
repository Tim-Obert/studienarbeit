import Vue from 'vue'
import RecordingsService from "@/services/RecordingsService";
import {RecordingInterface} from "@/interfaces/RecordingInterface";

export const recordingsStoreState = Vue.observable({
    allRecordingsArray: new Array<RecordingInterface>(),
    recordingsArray: new Array<RecordingInterface>()
})

export const recordingsStoreMutations = {
    getList: async () => {
        const recordingsService = new RecordingsService();
        recordingsStoreState.recordingsArray = await recordingsService.getRecordings()
        recordingsStoreState.allRecordingsArray = recordingsStoreState.recordingsArray
    },
    sortByCamera: () => {
        recordingsStoreState.recordingsArray.filter(x => x.camera !== null).sort(function (a: RecordingInterface, b: RecordingInterface) {
            if (a.camera === null || b.camera === null) {
                return 0;
            }
            if (a.camera.name < b.camera.name) {
                return -1;
            }
            if (a.camera.name < b.camera.name) {
                return 1;
            }
            return 0;
        })
    },
     sliceByCameraName: (camera: string) => {
        recordingsStoreState.recordingsArray = recordingsStoreState.allRecordingsArray.filter((video: RecordingInterface) => {
             return video.camera?.name === camera || camera === ""
         });
     }
}
