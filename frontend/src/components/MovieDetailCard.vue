<template>
  <div class="movie-detail-card">
    <div class="card-header">
      <h1 class="movie-title">{{ movieTitle }}</h1>
    </div>
    
    <div class="card-body">
      <div class="description-section">
        <h3>Описание</h3>
        <p class="movie-description">{{ movieDescription }}</p>
      </div>
      
      <div class="suggestion-meta">
        <div class="meta-item">
          <strong>Предложил:</strong>
          <span>{{ suggesterName }}</span>
        </div>
        
        <div class="meta-item">
          <strong>Дата предложения:</strong>
          <span>{{ formattedDate }}</span>
        </div>
        
        <div class="meta-item">
          <strong>Статус:</strong>
          <span class="status-badge">На рассмотрении</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieDetailCard',
  props: {
    suggestion: {
      type: Object,
      required: true
    }
  },
  computed: {
    movieTitle() {
      return this.suggestion.movie?.title || 'Без названия'
    },
    movieDescription() {
      return this.suggestion.movie?.description || 'Описание отсутствует'
    },
    suggesterName() {
      if (this.suggestion.is_anonymous) {
        return 'Аноним'
      }
      return this.suggestion.suggester_name || 'Не указано'
    },
    formattedDate() {
      if (!this.suggestion.created_at) return 'Дата не указана'
      return new Date(this.suggestion.created_at).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.movie-detail-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  color: white;
}

.movie-title {
  margin: 0;
  font-size: 2rem;
  text-align: center;
}

.card-body {
  padding: 2rem;
}

.description-section {
  margin-bottom: 2rem;
}

.description-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.movie-description {
  line-height: 1.6;
  color: #555;
  font-size: 1.1rem;
}

.suggestion-meta {
  border-top: 1px solid #ecf0f1;
  padding-top: 1.5rem;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.meta-item:last-child {
  border-bottom: none;
}

.meta-item strong {
  color: #2c3e50;
}

.status-badge {
  background: #ffeaa7;
  color: #e17055;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Мобильные стили */
@media (max-width: 768px) {
  .card-header {
    padding: 1.5rem;
  }
  
  .movie-title {
    font-size: 1.5rem;
  }
  
  .card-body {
    padding: 1.5rem;
  }
  
  .description-section h3 {
    font-size: 1.2rem;
  }
  
  .movie-description {
    font-size: 1rem;
    line-height: 1.5;
  }
  
  .suggestion-meta {
    padding-top: 1.25rem;
  }
  
  .meta-item {
    padding: 0.6rem 0;
  }
}

@media (max-width: 480px) {
  .card-header {
    padding: 1rem;
  }
  
  .movie-title {
    font-size: 1.3rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .description-section {
    margin-bottom: 1.5rem;
  }
  
  .description-section h3 {
    font-size: 1.1rem;
  }
  
  .movie-description {
    font-size: 0.95rem;
  }
  
  .meta-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .status-badge {
    font-size: 0.8rem;
    padding: 3px 8px;
  }
}
</style>