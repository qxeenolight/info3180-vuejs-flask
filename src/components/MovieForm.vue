<template>
    <form @submit.prevent="saveMovie" id="movieForm">
        <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
            {{ message }}
        </div>
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control" required/>
        </div>

        <div class="form-group mb-3">
            <label for="description" class="form-label">Movie Description</label>
            <input type="text" name="description" class="form-control" required/>
        </div>

        <div class="form-group mb-3">
            <label for="photo" class="form-label">Poster</label>
            <!-- <input type="file" name="poster" class="form-control" /> -->
            <input type="file" name="photo" @change="handleFileChange" class="form-control">
        </div>

        <button type="submit" class="btn btn-primary">Save Movie</button>
    </form>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let message = ref("");
let selectedFile = null; // Track selected file
let success = ref(false); // Initialize success as false

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
    console.log(data);
    csrf_token.value = data.csrf_token;
})
} 

onMounted(() => {
    getCsrfToken();
});

const handleFileChange = (event) => {
    selectedFile = event.target.files[0]; // Update selected file
};

const saveMovie = () => {
    const form = document.querySelector("#movieForm");
    let formData = new FormData(form);

    fetch("/api/v1/movies", {
        method: 'POST',
        body: formData,
        headers: {
        'X-CSRFToken': csrf_token.value
        } 
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        console.log(data)
        if (data.success) {
            message.value = "File Uploaded Successfully.";
            success.value = true; // Set success to true
            form.reset(); // Reset the form
        } else {
            message.value = "Failed to save movie. Please check your input.";
        }
        console.log(data);
    })
    .catch(function (error) {
        console.log(error);
        message.value = "An error occurred while saving the movie.";
    });
};
</script>