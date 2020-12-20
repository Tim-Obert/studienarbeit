<template>
    <div class="recorded">
        <v-container>

                <div v-for="(recording, index) in recordings" :key="index">
                    <v-row>
                        {{recording}}
                        <div class="video">
                            <video :src="'http://localhost:8080/recordings/' + recording" controls/>
                        </div>
                    </v-row>
                    <hr>
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
                recordings: []
            }
        },
        created: function() {
            fetch("http://localhost:8080/recordings")
                .then((response) => {return response.json()})
                .then((data)  => {
                    this.$data.recordings = data;
                })
        }
    })
    export default class Recorded extends Vue {
    }
</script>
