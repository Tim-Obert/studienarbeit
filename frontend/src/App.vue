<template>
    <v-app>
        <v-app-bar
                app
                color="primary"
                dark
        >
            <v-btn to="/" text>Home</v-btn>
            <v-btn to="/overview" text>Overview</v-btn>
            <v-btn to="/recorded" text>Recorded</v-btn>
        </v-app-bar>
        <v-main>
            <v-container fluid>
                <router-view/>
            </v-container>
        </v-main>
    </v-app>
</template>

<script lang="ts">
    import Vue from 'vue';

    export default Vue.extend({
        name: 'App',

        components: {},

        data: () => ({
            //
        }),
    });
</script>
