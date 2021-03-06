<template>
  <div class="singleStream">
    <RTCStream :id="$route.params.id" :useStun="true" :autoplay="true"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import RTCStream from '@/components/RCTStream.vue'

@Component({
  components: {
    RTCStream
  },
})
export default class SingleStream extends Vue {}
</script>
