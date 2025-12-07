<template>
  <div class="movie-suggestion-card" @click="$emit('click')">
    <div class="card-content">
      <h3 class="movie-title">{{ movieTitle }}</h3>
      <p class="movie-description">{{ truncatedComment }}</p>
      <div class="suggestion-info">
        <span class="suggester">
          Offered by: {{ author }}
        </span>
        <span class="date">{{ formattedDate }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieSubmissionCard',
  props: {
    submission: {
      type: Object,
      required: true
    }
  },
  computed: {
    movieTitle() {
      return this.submission?.movie.title || 'No name'
    },
    comment() {
      return this.submission?.comment || 'No description'
    },
    truncatedComment() {
      const desc = this.comment
      return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
    },
    author() {
      if (this.submission?.is_anonymous) {
        return 'Anonymus'
      }
      return this.submission?.author || 'Anonymus'
    },
    formattedDate() {
      if (!this.submission?.created_at) return ''
      return new Date(this.submission.created_at).toLocaleDateString('ru-RU')
    }
  }
}
</script>>

<style scoped>
.movie-suggestion-card {
  background: white;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.movie-suggestion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.movie-title {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.movie-description {
  color: #666;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.suggestion-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.suggester {
  font-weight: 500;
}

.date {
  color: #95a5a6;
}

/* Мобильные стили */
@media (max-width: 768px) {
  .movie-suggestion-card {
    padding: 1.25rem;
  }
  
  .movie-title {
    font-size: 1.1rem;
  }
  
  .movie-description {
    font-size: 0.9rem;
    line-height: 1.4;
  }
  
  .suggestion-info {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .movie-suggestion-card {
    padding: 1rem;
  }
  
  .movie-title {
    font-size: 1rem;
    margin-bottom: 0.4rem;
  }
  
  .movie-description {
    font-size: 0.85rem;
    margin-bottom: 0.75rem;
  }
  
  .suggestion-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    font-size: 0.8rem;
  }
  
  @media (hover: none) {
    .movie-suggestion-card:hover {
      transform: none;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  }
}
</style>