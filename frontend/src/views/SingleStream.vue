<template>
  <div class="singleStream">
    <v-container>
      <v-row>
        <v-col>
        <RTCStream :id="parseInt($route.params.id, 10)" :useStun="true" :autoplay="true"/>
        </v-col>
        <v-col class="camera-attributes">
          <h1 class="heading">{{cam.name}}</h1>
          <p class="url"><strong>Url: </strong>{{cam.url}}</p>
          <p class="last-motion"><strong>Last motion: </strong>{{cam.getLastMotionAsDateString()}}</p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import RTCStream from '@/components/RTCStream.vue'
import {Camera} from "@/interfaces/CameraInterface";
import {cameraStoreMutations} from "@/store/CameraStore";

@Component({
  components: {
    RTCStream
  },
})
export default class SingleStream extends Vue {
  cam: Camera | undefined
  id = Number(this.$route.params.id)
  created() {
    this.cam = cameraStoreMutations.get(this.id)
  }
}
</script>

<style>

</style>
