import Vue from 'vue'
import VueRouter from 'vue-router'
import ProjectList from '@/views/ProjectList.vue'
import NewProject from '@/views/NewProject.vue'
import EditProject from '@/views/EditProject.vue'
import DatasetList from '@/views/DatasetList.vue'
import NewDataset from '@/views/NewDataset.vue'
import EditDataset from '@/views/EditDataset.vue'
import ExperimentList from '@/views/ExperimentList.vue'
import NewExperiment from '@/views/NewExperiment.vue'
import EditExperiment from '@/views/EditExperiment.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: ProjectList
  },
  {
    path: '/projects',
    name: 'projects',
    component: ProjectList
  },
  {
    path: '/projects/new',
    name: 'new-project',
    component: NewProject
  },
  {
    path: '/projects/edit',
    name: 'edit-project',
    component: EditProject
  },
  {
    path: '/datasets',
    name: 'datasets',
    component: DatasetList
  },
  {
    path: '/datasets/new',
    name: 'new-dataset',
    component: NewDataset
  },
  {
    path: '/datasets/edit',
    name: 'edit-dataset',
    component: EditDataset
  },
  {
    path: '/experiments',
    name: 'experiments',
    component: ExperimentList
  },
  {
    path: '/experiments/new',
    name: 'new-experiment',
    component: NewExperiment
  },
  {
    path: '/experiments/edit',
    name: 'edit-experiment',
    component: EditExperiment
  }
]

const router = new VueRouter({
  routes
})

export default router
