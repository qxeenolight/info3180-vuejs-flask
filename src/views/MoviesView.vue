<script setup>
import { ref, onMounted, computed } from "vue";

let moviesData = ref([]);

const fetchMovies = async () => {
    console.log("Fetching movies...");
    try {
        console.log("API Endpoint accessed...");
        const response = await fetch("/api/v1/movies");
        if (!response.ok) {
            console.log("Response not ok...");
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);
        moviesData.value = data.movies;
    } catch (error) {
        console.error("Error fetching movies:", error);
    }
};

onMounted(() => {
    fetchMovies();
});

const movies = computed(() => moviesData.value);

</script>

<template>
    <div :key="$route.fullPath">
        <h2>Movies</h2>
        <div class="card-group">
            <div v-for="movie in movies" :key="movie.id" class="card movie">
                <img :src="'../../uploads/' + movie.poster" class="card-img-top poster" alt="Movie Poster">
                <div class="card-body details">
                    <h5 class="card-title">{{ movie.title }}</h5>
                    <p class="card-text">{{ movie.description }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    h2 {
        margin-left: 160px;
        margin-bottom: 0;
    }

    .card-group {
        margin: auto;
        margin-left: 160px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 20px;
        max-width: 1200px;
    }

    .movie {
        height: 300px; /* Adjust height as needed */
        display: grid;
        grid-template-columns: 1fr 1fr;
        margin: 20px 0; /* Adjust margin to add gap */
        border-radius: 5px;
        box-shadow: 0 0 5px rgb(209, 209, 209);
    }

    .poster {
        width: 200px;
        height: 100%;
        border-radius: 5px 0 0 5px; /* Rounded corners on the left */
    }

    .details {
        padding: 15px;
        flex: 1;
    }
</style>