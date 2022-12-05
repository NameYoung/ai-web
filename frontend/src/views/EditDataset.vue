<template>
    <v-container>
        <v-alert dense outlined type="error" v-if="alert" dismissible>
            <strong>Request error:</strong> {{ errorMessage }}
        </v-alert>
        <v-row align="center" justify="center">
            <v-col cols="12">
                <v-card>
                    <v-card-title> Edit Dataset </v-card-title>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-text-field class="d-flex pa-6" v-model="id" :rules="idRules" label="Dataset Id" required
                            disabled></v-text-field>

                        <v-text-field class="d-flex pa-6" v-model="name" :counter="64" :rules="nameRules" label="Name"
                            required outlined></v-text-field>

                        <v-select class="d-flex pa-6" v-model="projectId" :items="projects" item-value="id"
                            item-text="name" label="Project" :rules="projectRules" required outlined
                            @click="getProjects"></v-select>

                        <v-textarea class="d-flex pa-6 overflow-auto" v-model="description" :rules="descriptionRules"
                            :counter="255" label="Description" outlined></v-textarea>

                        <div class="d-flex pa-6 overflow-auto">
                            <FileUpload @uploadSuccess="updateFileData" ref="fileUpload" :parentFileName="filePath">
                            </FileUpload>
                        </div>

                        <v-card height="500" elevation="0" class="d-flex overflow-auto">
                            <v-chart ref="scatter" class="chart" :option="option" />
                        </v-card>
                    </v-form>
                    <v-spacer></v-spacer>
                    <v-card-actions class="justify-center">
                        <v-btn :disabled="!valid" color="success" @click="updateDataset">
                            Update
                        </v-btn>

                        <v-btn color="error" class="d-flex ml-8" @click="cancelUpdateDataset">
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
import FileUpload from '@/components/FileUpload.vue'
export default {
    components: {
        FileUpload
    },
    mounted() {
        this.$data.id = this.$route.params.id
        this.$data.name = this.$route.params.name
        this.$data.projectId = this.$route.params.project_id
        this.$data.filePath = this.$route.params.file_path
        this.$data.description = this.$route.params.description
        this.$data.fileData = this.$route.params.data
        this.$data.option.series[0].data = this.$route.params.data
        this.$refs.fileUpload.uploadSuccess = true
        this.getProjects();
    },
    data: () => ({
        errorMessage: "",
        alert: false,
        valid: true,
        id: '',
        idRules: [
            v => !!v || 'Dataset id is required'
        ],
        name: '',
        nameRules: [
            v => !!v || 'Name is required',
            v => (v && v.length <= 64) || 'Name must be less than 64 characters',
        ],
        description: '',
        descriptionRules: [
            v => (v.length <= 255) || 'description must be less than 255 characters',
        ],
        projectId: null,
        projectRules: [
            v => !!v || 'Project is required',
        ],
        filePath: null,
        filePathRules: [
            v => !!v || 'File is required',
        ],
        fileData: [[]],
        projects: [],
        option: {
            xAxis: {
            },
            yAxis: {
            },
            series: [
                {
                    data: [[]],
                    type: 'scatter',
                }
            ]
        }
    }),
    methods: {
        validate() {
            return this.$refs.form.validate()
        },
        updateDataset() {
            if (this.validate() !== true) {
                return
            }
            if (this.filePath === null) {
                this.alertMessage("file can not be null")
                return
            }
            let self = this;
            this.$axios.put('/datasets/' + self.id, {
                id: self.id,
                name: self.name,
                description: self.description,
                project_id: self.projectId,
                file_path: self.filePath,
                data: self.fileData
            })
                .then(function () {
                    self.$router.push({
                        name: 'datasets'
                    })
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })

        },
        cancelUpdateDataset() {
            this.$router.push({
                name: 'datasets'
            })
        },
        getProjects() {
            let self = this;
            this.$axios.get('/projects')
                .then(function (response) {
                    self.projects = response.data;
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })
        },
        updateFileData() {
            this.filePath = this.$refs.fileUpload.filename
            this.fileData = this.$refs.fileUpload.fileData
            this.option.series[0].data = this.$refs.fileUpload.fileData
            this.$refs.scatter.chart.setOption(this.option);
        },
        alertMessage(message) {
            if (message) {
                this.alert = true
                this.errorMessage = message
                setTimeout(() => { this.alert = false }, 3000)
            }
        }
    },
}
</script>

<style>

</style>