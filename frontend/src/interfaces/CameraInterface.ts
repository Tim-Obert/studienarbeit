export interface CameraInterface {
    name: string;
    url: string;
    last_motion: number | null;
}

export class Camera implements CameraInterface{
    name: string;
    url: string;
    last_motion: number | null;

    public constructor(name: string, url: string, last_motion: number | null) {
        this.name = name;
        this.url = url;
        this.last_motion = last_motion;
    }
}
