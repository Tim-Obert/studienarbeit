<template>
    <div class="overview">
        <v-container>

            <div>
                <v-row>
                    <div class="camera" v-for="cam in cameraArray" :key="cam.id">
                        <v-card class="mx-auto mr-5 mt-5" max-width="400">
                            <div style="position: relative">
                                <img :src="streamPath + cam.id" :id="'stream.' + cam.id" width="100%"/>
                                <canvas :id="'overlay.' + cam.id" style="position: absolute; width: 100%; height: 100%; left: 0; top: 0;"></canvas>
                            </div>
                            <v-card-subtitle class="pb-0">
                                {{cam.name}}
                            </v-card-subtitle>

                            <v-card-text class="text--primary">
                                {{cam.url}}
                            </v-card-text>
                            <v-card-text class="text--primary">
                                Last Motion: {{cam.getLastMotionAsDateString()}}
                            </v-card-text>
                            <v-card-actions class="justify-center">
                                <v-btn color="orange" :to="'/stream/'+cam.id" text>
                                    Open
                                </v-btn>

                                <v-btn color="orange" text>
                                    <EditCameraDialog :cam="cam"/>
                                </v-btn>

                                <DeleteCameraDialog :cam="cam"/>
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
    import EditCameraDialog from "@/components/Camera/EditCameraDialog.vue";

    @Component({
        components: {
          EditCameraDialog,
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
            const connection = new WebSocket(process.env.VUE_APP_BACKEND_WS_URL)
            connection.onmessage = (e: any) => {
                const event = JSON.parse(e.data)
                if (event.event == "MotionResult" && event.data.motion) {
                    cameraStoreMutations.get(event.data.camera.id).last_motion = Date.now();
                    const image = document.getElementById('stream.' + event.data.camera.id) as HTMLImageElement;
                    if (image === null) {
                        return;
                    }
                    const scale = image.width / image.naturalWidth;
                    const canvas = document.getElementById('overlay.' + event.data.camera.id) as HTMLCanvasElement;
                    const ctx = canvas?.getContext('2d');
                    if (ctx === null) {
                        return;
                    }
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = 'blue';
                    event.data.boxes.forEach((box: number[]) => {
                        box = box.map(x => x*scale);
                        ctx.lineWidth = 5;
                        ctx.strokeStyle = 'green';
                        console.log(box);
                        ctx.strokeRect(box[0], box[1], box[2], -box[3]);
                    });
                }
            }
        },
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
