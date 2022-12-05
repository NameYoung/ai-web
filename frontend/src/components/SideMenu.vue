<template>
    <v-navigation-drawer v-model="drawer" :mini-variant.sync="mini" permanent app>
        <v-list-item class="px-2">
            <v-list-item-avatar>
                <v-img src="@/assets/admin.jpg"></v-img>
            </v-list-item-avatar>

            <v-list-item-title>Admin</v-list-item-title>

            <v-btn icon @click.stop="mini = !mini">
                <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-list dense>
            <v-list-item v-for="item in items" :key="item.title" @click="redirect(item.path)" link>
                <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    data() {
        return {
            drawer: true,
            items: [
                { title: 'Projects', icon: 'mdi-folder', path: 'projects' },
                { title: 'Datasets', icon: 'mdi-database', path: 'datasets' },
                { title: 'Experiments', icon: 'mdi-briefcase', path: 'experiments' },
            ],
            mini: true,
        }
    },
    methods: {
        redirect(path) {
            this.$router.push({
                name: path
            })
        }
    }
}
</script>