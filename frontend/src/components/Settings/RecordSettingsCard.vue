<template>
    <v-card width="500">
        <v-card-title>Recording</v-card-title>

        <v-card-text>
            <v-container fluid>
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
    export default {
        name: "RecordSettingsCard",
        data: () => ({
            settings: {
                frameBufferSize: 1000,
                videoPath: ""
            }
        }),
        methods: {
            snakeToCamel: (str) =>
                str.replace(
                /([-_][a-z])/g,
                (group) => group.toUpperCase()
                    .replace('-', '')
                    .replace('_', '')
            ),
            updateSettings(){
                return fetch('http://localhost:8080/settings', {
                    body: JSON.stringify(
                        this.settings
                    ),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'PUT'
                }).then( () => {
                    console.log(1);
                    location.reload();

                });
            }
        },
        created() {
            fetch('http://localhost:8080/settings')
                .then((response) => {return response.json()})
                .then((data)  => {
                    for(const setting in data) {
                        this.settings[this.snakeToCamel(setting)] = data[setting]
                    }
                })
        },
    }
</script>

<style scoped>

</style>
