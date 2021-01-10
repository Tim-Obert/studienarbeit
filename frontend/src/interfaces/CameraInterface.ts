export interface CameraInterface {
    name: string;
    url: string;
}

export class Camera implements CameraInterface{
    name: string;
    url: string;

    public constructor(name: string, url: string) {
        this.name = name;
        this.url = url;
    }
}
