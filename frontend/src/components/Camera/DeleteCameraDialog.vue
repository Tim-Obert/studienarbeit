<template>
    <v-dialog
            v-model="dialog"
            persistent
            max-width="600px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" color="orange" text>
                Delete
            </v-btn>
        </template>
        <v-card>
            <v-card-title class="headline">
                Are you sure?
            </v-card-title>
            <v-card-text>Do you really want to delete <strong>{{name}}</strong>?</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        color="orange"
                        text
                        @click="dialog = false"
                >
                    No
                </v-btn>
                <v-btn
                        color="orange"
                        text
                        @click="deleteCamera"
                >
                    Yes
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: "AddCameraDialog",
        data: function () {
            return {
                dialog: false
            }
        },
        props:{
          name: String
        },
        methods: {
            deleteCamera(){
                return fetch('http://localhost:8080/camera', {
                    body: JSON.stringify({
                        name: this.name
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'DELETE'
                }).then(() => {
                    this.dialog = false;
                    location.reload();
                });

            }
        }
    }
</script>

<style scoped>

</style>
