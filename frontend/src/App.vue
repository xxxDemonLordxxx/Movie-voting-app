<template>
  <div id="app">
    <div v-if="currentView === 'home'">
      <h1>Система предложения фильмов</h1>
      <button @click="showForm">Предложить фильм</button>
      <button @click="showSuggestions">Список предложений</button>
    </div>

    <div v-else-if="currentView === 'form'">
      <h2>Введите название фильма</h2>
      <input v-model="movieTitle" placeholder="Название фильма" />
      <button @click="submitMovie">Отправить</button>
      <button @click="goHome">Назад</button>
    </div>

    <div v-else-if="currentView === 'suggestions'">
      <h2>Список предложенных фильмов</h2>
      <div v-for="movie in movies" :key="movie.id" class="movie-item">
        {{ movie.title }}
      </div>
      <button @click="goHome">Назад</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentView: 'home',
      movieTitle: '',
      movies: []
    }
  },
  methods: {
    showForm() {
      this.currentView = 'form'
      this.movieTitle = ''
    },
    showSuggestions() {
      this.currentView = 'suggestions'
      this.fetchSuggestions()
    },
    goHome() {
      this.currentView = 'home'
    },
    async submitMovie() {
      if (!this.movieTitle.trim()) return

      try {
        const response = await fetch('http://localhost:8000/input', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ title: this.movieTitle })
        })

        if (response.ok) {
          alert('Фильм предложен успешно!')
          this.movieTitle = ''
          this.goHome()
        }
      } catch (error) {
        console.error('Error:', error)
        alert('Ошибка при отправке фильма')
      }
    },
    async fetchSuggestions() {
      try {
        const response = await fetch('http://localhost:8000/suggestions')
        if (response.ok) {
          this.movies = await response.json()
        }
      } catch (error) {
        console.error('Error:', error)
        alert('Ошибка при загрузке списка фильмов')
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

input {
  padding: 10px;
  font-size: 16px;
  margin: 10px;
  width: 300px;
}

.movie-item {
  padding: 10px;
  border-bottom: 1px solid #ccc;
  text-align: left;
}
</style>