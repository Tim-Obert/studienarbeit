<template>
    <div class="ws-streams">
        <v-skeleton-loader type="image" width="400px" height="300px" v-if="!loaded"/>
        <div class="streams__wrapper" v-if="loaded">
            <div class="stream float-left mr-12" v-for="(stream, index) in streams" :key="index">
                <img v-bind:src="stream">
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'WsStreams',
        data: function () {
            return {
                connection: null,
                streams: [],
                loaded: false
            }
        },
        props: {
            port: {
                type: String,
                required: true
            }
        },
        methods: {
        },
        created: function () {
            this.connection = new WebSocket('ws://localhost:' + this.port)
            this.connection.onmessage = function (event) {
                this.loaded = true;
                const data = JSON.parse(event.data)
                data.forEach(function (part, index) {
                    this[index] = 'data:image/jpeg;base64,' + this[index]
                }, data)
                this.streams = data
            }.bind(this)
        }
    }
</script>

<style>
    .v-skeleton-loader__image{
        height: 100% !important;
    }

</style>
