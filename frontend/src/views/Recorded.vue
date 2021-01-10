<template>
    <div class="recorded">
        <v-container>
            <v-row>
                <v-col>
                    <v-btn @click="sortByCamera">Sort by Cam name</v-btn>
                </v-col>
                <v-col>
                    <v-select :items="cameras" @change="sliceByCamera">
                    </v-select>
                </v-col>
            </v-row>

            <v-row>
                <div v-for="(video, index) in displayedVideos" :key="index">
                    <video-card :video="video"></video-card>
                </div>
            </v-row>
        </v-container>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import {VideoInterface} from '@/interfaces/VideoInterface';
    import VideoCard from "@/components/Video/VideoCard.vue";

    @Component({
        components: {
            VideoCard
        },
    })
    export default class Recorded extends Vue{
        allVideos = new Array<VideoInterface>();
        displayedVideos = new Array<VideoInterface>();
        cameras = [""];
        getVideos() {
            //todo: fetch from backend
            this.$data.allVideos.push(
                {
                    camera: "Cam1",
                    creationDateTime: "02.11.2020 13:37",
                    path: require("@/assets/videos/sample-mp4-file.mp4"),
                },
                {
                    camera: "Cam1",
                    creationDateTime: "03.11.2020 13:37",
                    path: require("@/assets/videos/sample-mp4-file.mp4"),
                },

                {
                    camera: "Cam2",
                    creationDateTime: "04.11.2020 13:37",
                    path: require("@/assets/videos/sample-mp4-file.mp4"),
                },
                {
                    camera: "Cam1",
                    creationDateTime: "04.11.2020 13:37",
                    path: require("@/assets/videos/sample-mp4-file.mp4"),
                },
            );
            this.displayedVideos = this.allVideos;
        }
        getCameras() {
            const camerasUnique = this.allVideos.map((video: VideoInterface) => video.camera)
                .filter((value: any, index: any, self: string | any[]) => self.indexOf(value) === index)
            this.cameras = this.cameras.concat(camerasUnique)
        }
        sortByCamera() {
            this.displayedVideos.sort(function (a: VideoInterface, b: VideoInterface) {
                if (a.camera < b.camera) {
                    return -1;
                }
                if (a.camera > b.camera) {
                    return 1;
                }
                return 0;
            })
        }
        sliceByCamera(camera: string){
            this.displayedVideos = this.allVideos.filter((video: VideoInterface) => {
                return video.camera === camera || camera === ""
            });
        }

        created() {
            this.getVideos();
            this.getCameras();
        }

    }
</script>
