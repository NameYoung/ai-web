<template>
    <v-container>
        <v-alert dense outlined type="error" v-if="alert" dismissible>
            <strong>Request error:</strong> {{ errorMessage }}
        </v-alert>
        <v-row align="center" justify="center">
            <v-col cols="12">
                <v-card>
                    <v-card-title> New Project </v-card-title>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-text-field class="d-flex pa-6" v-model="name" :counter="64" :rules="nameRules" label="Name"
                            required outlined></v-text-field>

                        <v-textarea class="d-flex pa-6 overflow-auto" v-model="description" :rules="descriptionRules"
                            :counter="255" label="Description" outlined></v-textarea>
                    </v-form>
                    <v-spacer></v-spacer>
                    <v-card-actions class="justify-center">
                        <v-btn :disabled="!valid" color="success" @click="createProject">
                            Create
                        </v-btn>

                        <v-btn color="error" class="d-flex ml-8" @click="cancelCreateProject">
                            Cancel
                        </v-btn>
                    </v-card-actions>
                    <v-spacer></v-spacer>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        errorMessage: "",
        alert: false,
        valid: true,
        name: '',
        nameRules: [
            v => !!v || 'Name is required',
            v => (v && v.length <= 64) || 'Name must be less than 64 characters',
        ],
        description: '',
        descriptionRules: [
            v => (v.length <= 255) || 'description must be less than 255 characters',
        ]
    }),

    methods: {
        validate() {
            return this.$refs.form.validate()
        },
        createProject() {
            if (this.validate() !== true) {
                return
            }
            let self = this;
            this.$axios.post('/projects', {
                name: self.name,
                description: self.description
            })
                .then(function () {
                    self.$router.push({
                        name: 'projects'
                    })
                })
                .catch(function (error) {
                    console.log(error)
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })

        },
        cancelCreateProject() {
            this.$router.push({
                name: 'projects'
            })
        }
    },
}
</script>

<style>

</style>