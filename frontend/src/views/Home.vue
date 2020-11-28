<template>
  <div class="home">
    Home
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
