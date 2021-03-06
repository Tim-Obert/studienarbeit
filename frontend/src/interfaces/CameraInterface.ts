export interface CameraInterface {
    id: number | null;
    name: string;
    url: string;
    last_motion: number | null;
}

export class Camera implements CameraInterface{
    id: number | null;
    name: string;
    url: string;
    last_motion: number | null;

    public constructor(id: number | null, name: string, url: string, last_motion: number | null) {
        this.id = id
        this.name = name
        this.url = url
        this.last_motion = last_motion
    }
}
