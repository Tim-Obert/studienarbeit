import ApiService from "@/services/ApiService"
import {Recording, RecordingInterface} from "@/interfaces/RecordingInterface";
import {cameraStoreMutations} from "@/store/CameraStore";

export default class RecordingsService {
    apiService = new ApiService()

    async getRecordings(): Promise<Array<RecordingInterface>> {
        const recordingArray = new Array<RecordingInterface>()
        return await this.apiService.get("/recordings")
            .then((responseBody) => {
                responseBody.map((recording: string)=>{
                    let recordingObj = new Recording(recording, null, '', null)
                    if (recording.match(RegExp("[0-9]*_[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]_.*"))){
                        recordingObj = this.filenameToRecording(recording)
                    }
                    recordingArray.push(recordingObj)
                })
                return recordingArray
            }).catch(() => {
                return recordingArray
            })
    }

    filenameToRecording(filename: string): RecordingInterface {
        const filenameWOExtension = filename.split('.').slice(0, -1).join('.')
        const filenameParts = filenameWOExtension.split('_')
        const camId = filenameParts[0]
        const camera = cameraStoreMutations.get(Number(camId))
        const creationDateParts = filenameParts[1].split("-")
        const creationTimeParts = filenameParts[2].split("-")
        const creationDateTime = new Date(Number(creationDateParts[2]), Number(creationDateParts[1]), Number(creationDateParts[0]), Number(creationTimeParts[0]), Number(creationTimeParts[1]), Number(creationTimeParts[2]))
        const trigger = filenameParts[3]
        return new Recording(filename, camera, trigger, creationDateTime)
    }

}
