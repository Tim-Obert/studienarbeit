import ApiService from "@/services/ApiService"
import {Settings} from "@/interfaces/SettingsInterface";



export default class SettingsService {
    apiService = new ApiService()

    updateSettings(settings: Settings){
        return this.apiService.put('/settings', settings)
    }

    getSettings(): Promise<Settings> {
        return this.apiService.get("/settings")
            .then((data)  => {
                return new Settings(data.frame_buffer_size, data.video_path)
            })
    }
}
