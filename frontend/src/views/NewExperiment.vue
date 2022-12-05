<template>
    <v-container>
        <v-alert dense outlined type="error" v-if="alert" dismissible>
            <strong>Request error:</strong> {{ errorMessage }}
        </v-alert>
        <v-row align="center" justify="center">
            <v-col cols="12">
                <v-card>
                    <v-card-title> New Experiment </v-card-title>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-text-field class="d-flex pa-6" v-model="name" :counter="64" :rules="nameRules" label="Name"
                            required outlined></v-text-field>

                        <v-select class="d-flex pa-6" v-model="projectId" :items="projects" item-value="id"
                            item-text="name" label="Project" :rules="projectRules" required outlined
                            @click="getProjects" @change="clearDataset"></v-select>

                        <v-select class="d-flex pa-6" v-model="datasetId" :items="datasets" item-value="id"
                            item-text="name" label="Dataset" :rules="datasetRules" required outlined
                            @click="getDatasets" @change="refreshSourceData"></v-select>

                        <v-card v-if="showSourceDataDiagram" height="500" elevation="0" class="d-flex overflow-auto">
                            <v-chart ref="sourceDataChart" class="chart" :option="sourceDataOption" />
                        </v-card>

                        <v-card elevation="0" class="d-flex">
                            <div class="pt-4 pl-6">
                                <h4>F2 Score :</h4>
                            </div>
                            <v-text-field v-model="r2Score" :rules="fitModelRules" required disabled
                                outlined></v-text-field>
                        </v-card>
                        <v-card v-if="showResultDiagram" height="500" elevation="0" class="d-flex overflow-auto">
                            <v-chart ref="resultChart" class="chart" :option="resultOption" />
                        </v-card>

                    </v-form>
                    <v-spacer></v-spacer>
                    <v-card-actions class="justify-center">
                        <v-btn :disabled="!valid" color="success" @click="createExperiment">
                            Create
                        </v-btn>

                        <v-btn color="error" class="d-flex ml-8" @click="cancelCreateExperiment">
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
    computed: {
        resultOption() {
            return {
                xAxis: {
                },
                yAxis: {
                },
                series: [
                    {
                        data: [[]],
                        type: 'scatter',
                    },
                    {
                        data: [[]],
                        type: 'line',
                        smooth: true
                    }
                ]
            }
        },
        sourceDataOption() {
            return {
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
        }
    },
    data() {
        return {
            errorMessage: "",
            alert: false,
            showSourceDataDiagram: false,
            showResultDiagram: false,
            valid: true,
            name: '',
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 64) || 'Name must be less than 64 characters',
            ],
            projectId: null,
            projectRules: [
                v => !!v || 'Project is required',
            ],
            datasetId: null,
            datasetRules: [
                v => !!v || 'Dataset is required',
            ],
            r2Score: null,
            fitModelRules: [
                v => !!v || 'Have to fit model',
            ],
            sourceData: [[]],
            predictData: null,
            predictIndex: null,
            model: null,
            projects: [],
            datasets: [],
        }
    },
    methods: {
        validate() {
            return this.$refs.form.validate()
        },
        createExperiment() {
            if (this.validate() !== true) {
                return
            }

            if (this.predictData === null) {
                this.alertMessage("predict can not be null")
                return
            }
            let self = this;
            this.$axios.post('/experiments', {
                name: self.name,
                project_id: self.projectId,
                dataset_id: self.datasetId,
                source_data: self.sourceData,
                predict_data: self.predictData,
                predict_index: self.predictIndex,
                model: self.model
            })
                .then(function () {
                    self.$router.push({
                        name: 'experiments'
                    })
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })

        },
        cancelCreateExperiment() {
            this.$router.push({
                name: 'experiments'
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
        getDatasets() {
            let self = this;
            this.$axios.get('/datasets', {
                params: {
                    project_id: self.projectId
                }
            })
                .then(function (response) {
                    self.datasets = response.data;
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })
        },
        fitModel(filePath) {
            let self = this;
            this.$axios.post('/fit-model', {
                file_path: filePath,
                model_type: 'LinearRegression'
            })
                .then(function (response) {
                    self.predictData = response.data.predict_data
                    self.predictIndex = response.data.predict_index
                    self.r2Score = response.data.predict_index.s2_score
                    self.model = response.data.model
                    self.refreshRsultData()
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })
        },
        refreshRsultData() {
            this.showResultDiagram = true
            this.resultOption.series[0].data = this.sourceData
            this.resultOption.series[1].data = this.predictData
            if(this.$refs.resultChart){
                this.$refs.resultChart.chart.setOption(this.resultOption)
            }
            
        },
        refreshSourceData(id) {
            this.showSourceDataDiagram = true
            var sourceDataset = this.datasets.find(x => x.id === id)
            this.sourceData = sourceDataset.data
            this.projectId = sourceDataset.project_id
            this.sourceDataOption.series[0].data = sourceDataset.data
            this.fitModel(sourceDataset.file_path)
            if(this.$refs.sourceDataChart){
                this.$refs.sourceDataChart.chart.setOption(this.sourceDataOption)
            }
        },
        clearDataset(){
            this.datasetId = null,
            this.sourceData = null
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