<template>
    <div class="overview">
      <WsStreams port="5678"/>
    </div>
</template>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import WsStreams from "@/components/WsStreams.vue";

  @Component({
    components: {
      WsStreams

    },
  })
  export default class Overview extends Vue {}
</script>
