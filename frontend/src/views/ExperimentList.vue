<template>
    <v-container fluid>
        <v-alert dense outlined type="error" v-if="alert" dismissible>
            <strong>Request error:</strong> {{ errorMessage }}
        </v-alert>
        <div>
            <h2 class="text-left">
                Datasets
            </h2>
        </div>
        <v-row no-gutters style="height: 60px;">
            <v-col class="d-flex" cols="3">
                <v-select :items="projects" item-value="id" item-text="name" label="Filter by Project"></v-select>
            </v-col>

            <v-col class="text-right">
                <v-btn color="success" elevation="2" @click="createDataset">New Dataset</v-btn>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-data-table height="600" :headers="headers" :items="projects" :items-per-page="15" class="elevation-2"
            no-data-text="No Data">
            <template v-slot:[`item.actions`]="{ item }">
                <v-icon small class="mr-2" @click="editProject(item)">
                    mdi-pencil
                </v-icon>
                <v-icon small @click="deleteProject(item)">
                    mdi-delete
                </v-icon>
            </template>
        </v-data-table>
        <v-dialog v-model="dialogDelete" max-width="320">
            <v-card>
                <v-card-title class="headline">Confirm</v-card-title>
                <v-card-text>Are you sure you want to delete this item?</v-card-text>

                <v-card-actions class="justify-center">
                    <v-spacer></v-spacer>
                    <v-btn color="blue" class="d-flex white--text" @click="cancelDelete">
                        Cancel
                    </v-btn>

                    <v-btn color="error" class="d-flex ml-8 white--text" @click="confirmDelete">
                        Confirm
                    </v-btn>
                    <v-spacer></v-spacer>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>

</template>
  
<script>

export default {
    data() {
        return {
            dialogDelete: false,
            deleteProjectId: null,
            filters: [],
            errorMessage: "",
            alert: false,
            totalCount: 0,
            headers: [
                {
                    text: 'Id',
                    align: 'start',
                    sortable: false,
                    value: 'id',
                },
                { text: 'Name', value: 'name' },
                { text: 'Project', value: 'project.name' },
                { text: 'Description', value: 'description' },
                { text: 'Create At', value: 'created_at' },
                { text: 'Updated At', value: 'updated_at' },
                { text: 'Action', value: 'actions', sortable: false }
            ],
            datasets: [],
            projects: []
        }
    },
    mounted() {
        this.getProjects()
    },
    methods: {
        createDataset() {
            this.$router.push({
                name: 'new-dataset'
            })
        },
        editProject(item) {
            this.$router.push({
                name: 'edit-project',
                params: item
            })
        },
        deleteProject(item) {
            this.deleteProjectId = item.id
            this.dialogDelete = true
        },
        getDatasets() {
            let self = this;
            this.$axios.get('/datasets')
                .then(function (response) {
                    self.datasets = response.data;
                    self.totalCount = self.projects.length
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
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
        confirmDelete() {
            let self = this;
            this.$axios.delete('/projects/' + self.deleteProjectId)
                .then(function () {

                })
                .catch(function (error) {
                    console.log(error)
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })
            this.dialogDelete = false
            this.$router.go()
        },
        cancelDelete() {
            this.deleteProjectId = null
            this.dialogDelete = false
        },
        alertMessage(message) {
            if (message) {
                this.alert = true
                this.errorMessage = message
                setTimeout(() => { this.alert = false }, 3000)
            }
        }
    }
}
</script>
  
<style lang="css">
tr {
    height: 60px !important;
}
</style>