<template>
    <div class="rtc-stream">
            <button id="start" v-on:click="start">Start1</button>


            <div id="media">
                <h2>Media</h2>

                <!--<audio id="audio" autoplay="true"></audio>
                <video id="video" autoplay="true" playsinline="true" controls width="500px"></video>-->
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
                pc: null
            }
        },
        props: {
            name: {
                type: String,
                required: true
            },
            autoplay: {
                type: Boolean
            }
        },
        methods: {
            start(){
                console.log(1);
                const config = {
                    sdpSemantics: 'unified-plan'
                };

                this.pc = new RTCPeerConnection(config);

                // connect audio / video
                this.pc.addEventListener('track', function(evt) {
                    const videotag = document.getElementById("Video-" + this.name);
                    if (videotag !== null) {
                        return;
                    }
                    const video = document.createElement('video');
                    video.id = "Video-" + this.name;
                    video.autoplay = true;
                    video.controls = true;
                    video.srcObject = evt.streams[0];
                    document.getElementById('media').append(video)
                    console.log(123)

                    /*if (evt.track.kind == 'video') {
                        document.getElementById('video').srcObject = evt.streams[0];
                    } else {
                        document.getElementById('audio').srcObject = evt.streams[0];
                    }*/
                });

                //document.getElementById('start').style.display = 'none';
                this.negotiate(this.pc);
            },
            negotiate(pc){
                pc.addTransceiver('video', {direction: 'recvonly'});
                pc.addTransceiver('audio', {direction: 'recvonly'});
                return pc.createOffer().then(function(offer) {
                    console.log(2);
                    return pc.setLocalDescription(offer);
                }).then(() => {
                    console.log(3);
                    // wait for ICE gathering to complete
                    return new Promise((resolve) => {
                        if (pc.iceGatheringState === 'complete') {
                            resolve();
                        } else {
                            console.log(5)
                            pc.addEventListener('icegatheringstatechange', this.checkState(pc, resolve));
                        }
                    });
                }).then(() => {
                    console.log(4);
                    const offer = pc.localDescription;
                    return fetch('http://localhost:8080/webrtc/offer', {
                        body: JSON.stringify({
                            sdp: offer.sdp,
                            type: offer.type,
                            name: this.name
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'POST'
                    });
                }).then(function(response) {
                    return response.json();
                }).then(function(answer) {
                    return pc.setRemoteDescription(answer);
                }).catch(function(e) {
                    alert(e);
                });
            },
            checkState(pc, resolve) {
                console.log(pc)
                if (pc.iceGatheringState === 'complete') {
                    pc.removeEventListener('icegatheringstatechange', this.checkState);

                    resolve();
                }
                resolve();
            }
        }
    }
</script>

<style scoped>

</style>
