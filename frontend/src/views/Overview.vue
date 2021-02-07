<template>
    <div class="overview">
        <v-container>

            <div>
                <v-row>
                    <div class="camera" v-for="(cam, index) in cameraArray" :key="index">
                        <v-card class="mx-auto mr-5 mt-5" max-width="400">
                            <v-img :src="streamPath + cam.name" :id="'stream.' + cam.name"/>
                            <v-card-subtitle class="pb-0">
                                {{cam.name}}
                            </v-card-subtitle>

                            <v-card-text class="text--primary">
                                {{cam.url}}
                            </v-card-text>
                            <v-card-text class="text--primary">
                                Last Motion: {{timestampToString(cam.last_motion)}}
                            </v-card-text>
                            <v-card-actions class="justify-center">
                                <v-btn color="orange" :to="'/stream/'+cam.name" text>
                                    Open
                                </v-btn>

                                <v-btn color="orange" text>
                                    Edit
                                </v-btn>

                                <DeleteCameraDialog :name="cam.name"/>
                            </v-card-actions>
                        </v-card>
                    </div>

                    <div class="camera__add">
                        <v-card class="mx-auto mr-5 mt-5" width="320" height="240">
                            <v-card-actions class="addBtn__wrapper justify-center align-center">
                                <AddCameraDialog/>
                            </v-card-actions>
                        </v-card>
                    </div>

                </v-row>
            </div>

        </v-container>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import WsStreams from "@/components/WsStreams.vue";
    import AddCameraDialog from "@/components/Camera/AddCameraDialog.vue";
    import DeleteCameraDialog from "@/components/Camera/DeleteCameraDialog.vue";
    import {cameraStoreMutations, cameraStoreState} from "@/store/CameraStore";

    @Component({
        components: {
            WsStreams,
            AddCameraDialog,
            DeleteCameraDialog
        },
        data: function () {
            return {
                streamPath: process.env.VUE_APP_BACKEND_URL + "/streams/",
                dialog: false,
            }
        },
        computed: {
            cameraArray() {
                return cameraStoreState.camerasArray;
            }
        },
        created: async function () {
            await cameraStoreMutations.getList()

            //WS-Socket for Motion
            const connection = new WebSocket('ws://localhost:5678')
            connection.onmessage = function (e: any) {
                const event = JSON.parse(e.data)
                if (event.event == "MotionResult") {
                    cameraStoreMutations.get(event.data.camera.name).last_motion = Date.now();
                }
            }
        },
        methods: {
            timestampToString(timestamp: Date) {
                if (timestamp == null) {
                    return "-";
                }
                return new Date(timestamp).toUTCString();
            }
        }
    })
    export default class Overview extends Vue {
    }
</script>

<style>
    .addBtn__wrapper {
        height: 100%
    }

    .addBtn__wrapper .addBtn {
        width: 50px;
    }

    .motion {
        border: 2px solid red
    }
</style>
