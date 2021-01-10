<template>
    <v-dialog
            v-model="dialog"
            persistent
            max-width="600px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" color="orange" text>
                Delete
            </v-btn>
        </template>
        <v-card>
            <v-alert
                    v-if="error"
                    dense
                    outlined
                    type="error"
            >
                {{errorMessage}}
            </v-alert>
            <v-card-title class="headline">
                Are you sure?
            </v-card-title>
            <v-card-text>Do you really want to delete <strong>{{name}}</strong>?</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        color="orange"
                        text
                        @click="dialog = false"
                >
                    No
                </v-btn>
                <v-btn
                        color="orange"
                        text
                        @click="deleteCamera"
                >
                    Yes
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import CameraService from "../../services/CameraService"

    const cameraService = new CameraService
    export default {
        name: "AddCameraDialog",
        data: function () {
            return {
                dialog: false,
                error: false,
                errorMessage: false
            }
        },
        props:{
          name: String
        },
        methods: {
            deleteCamera(){
                cameraService.removeCamera(this.name)
                    .then((res) => {
                        if(res.status === 204) {
                           this.dialog = false
                        }else {
                            this.error = true
                            this.errorMessage = "Error"
                            //TODO: error handling, if backend responses with errors
                        }
                }).catch((err) => {
                    this.error = true
                    this.errorMessage = "Error: " + err
                    //TODO: error handling, if backend responses with errors
                })
            }
        }
    }
</script>

<style scoped>

</style>
