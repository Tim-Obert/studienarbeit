export interface SettingsInterface {
    frameBufferSize: number;
    videoPath: string;
}

export class Settings implements SettingsInterface {
    frameBufferSize: number;
    videoPath: string;

    public constructor(frameBufferSize: number, videoPath: string) {
        this.frameBufferSize = frameBufferSize;
        this.videoPath = videoPath;
    }

}
