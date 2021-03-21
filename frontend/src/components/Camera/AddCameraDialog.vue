<template>
    <v-dialog
            v-model="dialog"
            persistent
            max-width="600px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                    v-bind="attrs"
                    v-on="on"
                    class="mx-2"
                    fab
                    dark
                    color="orange"

            >
                <v-icon dark>
                    mdi-plus
                </v-icon>
            </v-btn>
        </template>
        <v-card>
            <v-card-title>
                <span class="headline">Add Camera</span>
            </v-card-title>
            <v-card-text>
                <v-alert
                        v-if="error"
                        dense
                        outlined
                        type="error"
                >
                    {{errorMessage}}
                </v-alert>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                    label="name"
                                    required
                                    v-model="name"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                    label="url"
                                    type="text"
                                    required
                                    v-model="url"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
                <small>*indicates required field</small>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        color="blue darken-1"
                        text
                        @click="dialog = false"
                >
                    Close
                </v-btn>
                <v-btn
                        color="blue darken-1"
                        text
                        @click="addCamera()"
                >
                    Save
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import CameraService from "../../services/CameraService"
    import {Camera} from "@/interfaces/CameraInterface";
    const cameraService = new CameraService
    export default {
        name: "AddCameraDialog",
        data: function () {
            return {
                dialog: false,
                name: '',
                url: '',
                error: false,
                errorMessage: ''
            }

        },
        methods: {
            async addCamera() {
                await cameraService.addCamera(new Camera(null, this.name, this.url, null))
                    .then((res) => {
                        if (res.status === 201) {
                            this.dialog = false
                        } else {
                            this.error = true
                            this.errorMessage = "Error"
                            //TODO: error handling, if backend responses with errors
                        }
                })
            }
        }
    }
</script>

<style scoped>

</style>
