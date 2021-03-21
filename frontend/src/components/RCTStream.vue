<template>
    <div class="rtc-stream__wrapper">
        <div id="media">
            <v-skeleton-loader type="image" width="600px" height="300px" v-if="!loaded"/>
            <video v-if="loaded" id="video" src="#" :srcObject.prop="streamObject"  playsinline autoplay controls width="600px"></video>
        </div>
    </div>

</template>

<script>
    export default {
        name: "RCTStream",
        data: function () {
            return {
                loaded: false,
                stream: null,
                pc: null,
                streamObject: null
            }
        },
        props: {
            id: {
                type: Number,
                required: true
            },
            useStun: {
                type: Boolean
            },

        },
        methods: {
            negotiate(pc, id) {
                pc.addTransceiver('video', {direction: 'recvonly'});
                pc.addTransceiver('audio', {direction: 'recvonly'});
                return pc.createOffer().then(function (offer) {
                    return pc.setLocalDescription(offer);
                }).then(function () {
                    // wait for ICE gathering to complete
                    return new Promise(function (resolve) {
                        if (pc.iceGatheringState === 'complete') {
                            resolve();
                        } else {
                            pc.addEventListener('icegatheringstatechange', function check() {
                                if (pc.iceGatheringState === 'complete') {
                                    pc.removeEventListener('icegatheringstatechange', check);
                                    resolve();
                                }
                            });
                        }
                    });
                }).then(function () {
                    const offer = pc.localDescription;
                    return fetch('/webrtc/offer', {
                        body: JSON.stringify({
                            sdp: offer.sdp,
                            type: offer.type,
                            id: id
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'POST'
                    });
                }).then(function (response) {
                    return response.json();
                }).then(function (answer) {
                    return pc.setRemoteDescription(answer);
                }).catch(function (e) {
                    alert(e);
                });
            },
            start() {
                const config = {
                    sdpSemantics: 'unified-plan'
                };

                if (this.useStun) {
                    config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];
                }

                const pc = new RTCPeerConnection(config);


                // connect audio / video
                pc.addEventListener('track', function (evt) {
                    this.streamObject = evt.streams[0];
                    this.loaded = true;
                }.bind(this));
                this.negotiate(pc, this.id);
            },

        },
        created() {
            this.start();
        }
    }
</script>

<style scoped>

</style>
