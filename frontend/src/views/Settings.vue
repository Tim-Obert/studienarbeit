<template>
    <div class="settings">
        <v-container>
            <v-row>
                <record-settings-card />

            </v-row>
        </v-container>

    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import RecordSettingsCard from "@/components/Settings/RecordSettingsCard.vue";

    @Component({
        components: {
            RecordSettingsCard
        },


    })
    export default class Settings extends Vue {
    }
</script>
