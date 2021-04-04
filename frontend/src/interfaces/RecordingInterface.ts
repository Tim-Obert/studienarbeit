import {Camera} from "@/interfaces/CameraInterface";

export interface RecordingInterface {
    filename: string;
    camera: Camera | null;
    trigger: string;
    creationDateTime: Date | null;

    getCreationDateTimeAsDateString(): string;
}

export class Recording implements RecordingInterface {
    filename: string;
    camera: Camera | null;
    trigger: string;
    creationDateTime: Date | null;

    public constructor(filename: string, camera: Camera | null, trigger: string, creationDateTime: Date | null){
        this.filename = filename
        this.camera = camera
        this.trigger = trigger
        this.creationDateTime = creationDateTime
    }

    public getCreationDateTimeAsDateString(): string {
        if (this.creationDateTime == null) {
            return "-"
        }
        return new Date(this.creationDateTime).toUTCString();
    }

}
