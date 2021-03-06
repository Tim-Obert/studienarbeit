<template>
  <v-card class="mx-auto mr-5 mt-5" max-width="400">
    <video :src="video.path" controls/>
    <v-card-title>
      {{ video.camera }}
    </v-card-title>

    <v-card-subtitle class="pb-0">
      {{ video.creationDateTime }}
    </v-card-subtitle>

    <v-card-text class="text--primary">
      {{ video.url }}
    </v-card-text>
    <v-card-actions class="justify-center">
      <v-btn class="mx-2" @click="download" fab dark small color="orange">
        <v-icon dark>
          mdi-download
        </v-icon>
      </v-btn>
      <v-btn class="mx-2" @click="remove" fab dark small color="orange">
        <v-icon dark>
          mdi-delete
        </v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {VideoInterface} from "@/interfaces/VideoInterface";

export default {
  name: "VideoCard",
  props: {
    video: VideoInterface
  },
  methods: {
    download() {
      //todo: download
      alert("download")
    },
    remove() { // method can't be named in "delete"
      //todo: remove
      alert("remove")
    },
  }
}
</script>

<style scoped>

</style>
