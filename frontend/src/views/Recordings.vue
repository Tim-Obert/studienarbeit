<template>
    <div class="recorded">
        <v-container>
            <v-row>
                <v-col>
                    <v-btn @click="sortByCamera">Sort by Cam name</v-btn>
                </v-col>
                <v-col>
                    <v-select :items="camerasArray" :item-text="'name'" :item-value="'name'" label="Select camera" @change="sliceByCameraName">
                      <v-item value="''"> </v-item>
                    </v-select>
                </v-col>
            </v-row>

            <v-row>
                <div v-for="(video, index) in recordingsArray" :key="index">
                    <video-card :video="video"></video-card>
                </div>
            </v-row>
        </v-container>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import VideoCard from "@/components/Video/VideoCard.vue";
    import {recordingsStoreMutations, recordingsStoreState} from "@/store/RecordingsStore";
    import {cameraStoreMutations, cameraStoreState} from "@/store/CameraStore";
    import {Camera} from "@/interfaces/CameraInterface";

    @Component({
        components: {
            VideoCard
        },
      computed: {
        recordingsArray() {
          return recordingsStoreState.recordingsArray;
        },
        camerasArray() {
          const camerasArray = cameraStoreState.camerasArray
          return [new Camera(null, "", "", null)].concat(camerasArray);
        }
      },
      methods: {
        sortByCamera() {
          recordingsStoreMutations.sortByCamera()
        },
        sliceByCameraName(camera: string) {
          recordingsStoreMutations.sliceByCameraName(camera)
        }
      },
      created: async function () {
        await recordingsStoreMutations.getList()
        await cameraStoreMutations.getList()
      }
    })
    export default class Recordings extends Vue{}
</script>
