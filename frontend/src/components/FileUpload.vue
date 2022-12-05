<template>
    <v-row>
        <v-col cols="6">
            <v-file-input accept=".csv" :label="parentFileName" @change="selectFile"
                @click:clear="clearFile" outlined>
                <template v-slot:append-outer>
                    <v-icon v-if="uploadSuccess" color="green">
                        mdi-checkbox-marked-circle
                    </v-icon>
                </template>
            </v-file-input>
            <v-alert dense outlined type="error" v-if="alert" dismissible>
                <strong>Upload error:</strong> {{ errorMessage }}
            </v-alert>
        </v-col>
    </v-row>

</template>

<script>
export default {
    data() {
        return {
            file: null,
            filename: null,
            fileData: [[]],
            uploadSuccess: false,
            fileUploaded: true,
            errorMessage: null,
            alert: false,
        }
    },
    methods: {
        selectFile(file) {
            this.uploadSuccess = false
            this.file = file
            this.uploadFile()
        },
        uploadFile() {
            if (this.file === null) {
                this.alertMessage("Must choosr a file")
                return
            }
            var formData = new FormData();
            formData.append("file", this.file);
            let self = this;
            this.$axios.post('/upload-file', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
                .then(function (response) {
                    self.uploadSuccess = true
                    self.filename = response.data.filename
                    self.fileData = response.data.file_data
                    self.$emit('uploadSuccess')
                })
                .catch(function (error) {
                    if (error.response.data.detail) {
                        self.alertMessage(error.response.data.detail)
                    }
                })
        },
        clearFile() {
            this.uploadSuccess = false
            this.file = null
            this.filename = null
        },
        alertMessage(message) {
            if (message) {
                this.alert = true
                this.errorMessage = message
                setTimeout(() => { this.alert = false }, 3000)
            }
        }
    },
    props: ['parentFileName']
}
</script>

<style>

</style>