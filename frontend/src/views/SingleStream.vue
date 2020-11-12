<template>
  <div class="singleStream">
    <RTCStream :name="$route.params.id" :useStun="true" :autoplay="true"/>
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
export default class Home extends Vue {}
</script>
