<template>
  <v-container fluid>
    <v-alert dense outlined type="error" v-if="alert" dismissible>
      <strong>Request error:</strong> {{ errorMessage }}
    </v-alert>
    <div>
      <h2 class="text-left">
        Projects
      </h2>
    </div>
    <v-row no-gutters style="height: 60px;">
      <v-col class="d-flex" cols="3">

      </v-col>

      <v-col class="text-right">
        <v-btn color="success" elevation="2" @click="createProject">New Project</v-btn>
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
      <template v-slot:[`item.datasets`]="{ item }">
        <v-chip>
          datasets
          <v-icon @click="redirectDatasets(item)">
            mdi-link
          </v-icon>
        </v-chip>

      </template>
      <template v-slot:[`item.experiments`]="{ item }">
        <v-chip>
          experiments
          <v-icon @click="redirectExperiments(item)">
            mdi-link
          </v-icon>
        </v-chip>

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
        { text: 'Description', value: 'description' },
        { text: 'Create At', value: 'created_at' },
        { text: 'Updated At', value: 'updated_at' },
        { text: 'Datasets', value: 'datasets', sortable: false },
        { text: 'Experiments', value: 'experiments', sortable: false },
        { text: 'Action', value: 'actions', sortable: false }
      ],
      projects: []
    }
  },
  created() {
    this.getProjects()
  },
  methods: {
    createProject() {
      this.$router.push({
        name: 'new-project'
      })
    },
    redirectDatasets(item) {
      this.$router.push({
        name: 'datasets',
        params: item
      })
    },
    redirectExperiments(item) {
      this.$router.push({
        name: 'experiments',
        params: item
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
    getProjects() {
      let self = this;
      this.$axios.get('/projects')
        .then(function (response) {
          self.projects = response.data;
          self.totalCount = self.projects.length
        })
        .catch(function (error) {
          console.log(error.response)
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