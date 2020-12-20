<template>
    <div class="recorded">
        <v-container>

                <div v-for="(video, index) in videos" :key="index">

                    {{video.creationDate}}
                    <v-row>
                    <div class="video" v-for="(path, index) in video.paths" :key="index">
                        <video :src="path" controls/>
                    </div>
                        
                    </v-row>
                    <hr />
                </div>

        </v-container>

    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';

    @Component({
        components: {},
        data: function () {
            return {
                videos: []
            }
        }


    })
    export default class Recorded extends Vue {
    }
</script>
