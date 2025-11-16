<template>
  <div class="home">
    <h1>Система предложения фильмов</h1>
    <div class="actions">
      <router-link to="/suggest" class="btn btn-primary">Предложить фильм</router-link>
    </div>
    
    <div class="suggestions-section">
      <h2>Предложенные фильмы</h2>
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">
        {{ error }}
        <button @click="fetchSuggestions" class="btn btn-secondary">Попробовать снова</button>
      </div>
      <div v-else-if="suggestions.length === 0" class="empty">
        Пока нет предложенных фильмов
      </div>
      <div v-else class="suggestions-list">
        <MovieSuggestionCard 
          v-for="suggestion in suggestions" 
          :key="suggestion.id"
          :suggestion="suggestion"
          @click="viewSuggestion(suggestion.id)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import MovieSuggestionCard from '@/components/MovieSuggestionCard.vue'

export default {
  name: 'HomePage',
  components: {
    MovieSuggestionCard
  },
  data() {
    return {
      suggestions: [],
      loading: false,
      error: null
    }
  },
  async mounted() {
    await this.fetchSuggestions()
  },
  methods: {
    async fetchSuggestions() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch('http://localhost:8000/suggestions')
        if (response.ok) {
          this.suggestions = await response.json()
          console.log('Loaded suggestions:', this.suggestions) // Для отладки
        } else {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
      } catch (error) {
        console.error('Error loading suggestions:', error)
        this.error = 'Ошибка при загрузке списка фильмов: ' + error.message
      } finally {
        this.loading = false
      }
    },
    viewSuggestion(id) {
      this.$router.push(`/suggestion/${id}`)
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
}

.actions {
  margin: 2rem 0;
}

.btn {
  display: inline-block;
  padding: 12px 24px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  margin: 0.5rem;
}

.btn-primary {
  background-color: #3498db;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.suggestions-section {
  margin-top: 2rem;
  text-align: left;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.loading, .empty, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

/* Мобильные стили */
@media (max-width: 768px) {
  .home h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .suggestions-section h2 {
    font-size: 1.3rem;
  }
  
  .btn {
    padding: 10px 20px;
    font-size: 14px;
    margin: 0.25rem;
  }
  
  .actions {
    margin: 1.5rem 0;
  }
  
  .suggestions-section {
    margin-top: 1.5rem;
  }
}

@media (max-width: 480px) {
  .home h1 {
    font-size: 1.3rem;
  }
  
  .suggestions-section h2 {
    font-size: 1.2rem;
  }
  
  .btn {
    padding: 8px 16px;
    font-size: 13px;
    width: 100%;
    margin: 0.25rem 0;
  }
  
  .actions {
    margin: 1rem 0;
  }
  
  .loading, .empty, .error {
    padding: 1.5rem;
    font-size: 0.9rem;
  }
}
</style>