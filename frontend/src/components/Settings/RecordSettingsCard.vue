<template>
    <v-card width="500">
        <v-card-title>Recording</v-card-title>

        <v-card-text>
            <v-container fluid>
                <v-alert
                        v-if="error"
                        dense
                        outlined
                        type="error"
                >
                    {{errorMessage}}
                </v-alert>

                <v-alert
                        v-if="success"
                        dense
                        outlined
                        type="success"
                >
                    Settings updated
                </v-alert>
                <v-row>
                    <v-tooltip top>
                        <template v-slot:activator="{ on, attrs }">
                            <v-col cols="12" v-bind="attrs"
                                   v-on="on">
                                <v-slider
                                        v-model="settings.frameBufferSize"
                                        :max="3000"
                                        :min="100"
                                        label="Frame Buffer"
                                        class="align-center"
                                >
                                    <template v-slot:append>
                                        <v-text-field
                                                v-model="settings.frameBufferSize"
                                                class="mt-0 pt-0"
                                                type="number"
                                                style="width: 60px"
                                        ></v-text-field>
                                    </template>
                                </v-slider>
                            </v-col>
                        </template>
                        <span>Frames that are stored before a Motion is tracked</span>
                    </v-tooltip>

                </v-row>
                <v-row>
                    <v-col cols="12">
                        <v-text-field label="Path where the recorded videos are stored" v-model="settings.videoPath"></v-text-field>
                    </v-col>
                </v-row>
            </v-container>
        </v-card-text>

        <v-btn
                class="ma-3 float-right"
                color="primary"
                dark
                @click="updateSettings"
        >
            Save
            <v-icon
                    dark
                    right
            >
                mdi-checkbox-marked-circle
            </v-icon>
        </v-btn>
    </v-card>
</template>

<script>
    import SettingsService from "@/services/SettingsService";
    import {Settings} from "@/interfaces/SettingsInterface";

    const settingsService = new SettingsService()
    export default {
        name: "RecordSettingsCard",
        data: () => ({
            settings: new Settings(1000, ""),
            success: false,
            error: false,
            errorMessage: ""
        }),
        methods: {
            updateSettings(){
                settingsService.updateSettings(this.settings).then((res) => {
                    if (res.status === 201) {
                        this.showAlert(true)
                        setTimeout(() => this.success = false, 3000);
                    }else {
                        this.showAlert(false, 'Server failure')
                    }
                }).catch((err) => {
                    this.showAlert(false, "Error: "+ err.message)
                })
            },
            showAlert(success, errorMessage) {
                this.success = success;
                this.error = !success;
                this.errorMessage = errorMessage;
            }
        },
        created() {
            settingsService.getSettings().then((res) => {
                this.settings = res
            }).catch((err) => {
                this.showAlert(false, "Error: "+ err.message)
            })
        },
    }
</script>

<style scoped>

</style>
