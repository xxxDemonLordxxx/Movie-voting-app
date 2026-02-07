<script setup>
import { ref, watch, onUnmounted } from 'vue'

const query = ref('')
const movies = ref([])
const loading = ref(false)
const showDropdown = ref(false)

let debounceTimer
const searchMovies = async () => {
  try {
    const url = `http://backend:8000/films/search/${encodeURIComponent(query.value)}`
    console.log('Fetching URL:', url)  // Debug
    
    const res = await fetch(url)
    console.log('Response status:', res.status)  // Debug
    console.log('Response headers:', [...res.headers.entries()])  // Debug
    
    const text = await res.text()
    console.log('Raw response (first 500 chars):', text.substring(0, 500))  // Debug
    
    // Check if it's JSON
    if (res.headers.get('content-type')?.includes('application/json')) {
      movies.value = JSON.parse(text)
    } else {
      console.error('Response is not JSON!', text)
      movies.value = []
    }
  } catch (error) {
    console.error('Search error:', error)
  }
}
// Debounce search
watch(query, () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(searchMovies, 300)
})

// Close dropdown
const closeDropdown = () => showDropdown.value = false

// Handle selection
const selectMovie = (movie) => {
  query.value = movie.title
  closeDropdown()
  // Fetch full movie data
  fetch(`/movies/${movie.id}`)
    .then(res => res.json())
    .then(data => console.log('Selected movie:', data))
}
</script>

<template>
  <div class="search-container">
    <input 
      v-model="query" 
      @focus="showDropdown = movies.length > 0"
      placeholder="search"
      class="form-input"
    />
    
    <div v-if="loading">Loading...</div>
    
    <div v-if="showDropdown" class="dropdown">
      <div 
        v-for="movie in movies" 
        :key="movie.id"
        @click="selectMovie(movie)"
        class="dropdown-item"
      >
        {{ movie.title }}
        <span v-if="movie.language">({{ movie.language }})</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-container { position: relative; }
.dropdown {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
}
.dropdown-item {
  padding: 8px;
  cursor: pointer;
}
.dropdown-item:hover { background: #f0f0f0; }
</style>