<template>
  <v-card class="mx-auto mr-5 mt-5" max-width="400">
    <video :src="'recordings/' +video.filename" controls/>
    <v-card-title>
      {{ video.getCreationDateTimeAsDateString() }}
    </v-card-title>

    <v-card-subtitle class="pb-0">
      {{ video.filename }}
    </v-card-subtitle>

    <v-card-text class="text--primary" v-if="video.camera != null">
      Camera: {{video.camera.name}}
    </v-card-text>
  </v-card>
</template>

<script>

import {Recording} from "@/interfaces/RecordingInterface";

export default {
  name: "VideoCard",
  props: {
    video: Recording
  },
}
</script>

<style scoped>
  video {
    width: 100%;
  }
</style>
