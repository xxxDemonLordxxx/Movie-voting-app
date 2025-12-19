<template>
  <div class="movie-suggestion-card" >
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
    <div class="more-button" @click="$emit('click')">MORE</div>
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
      return this.submission?.movie?.title || 'No name'
    },
    comment() {
      return this.submission.comment || 'No description'
    },
    truncatedComment() {
      const desc = this.comment
      return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
    },
    author() {
      if (this.submission.is_anonymous) {
        return 'Anonymus'
      }
      return this.submission.author || 'Anonymus'
    },
    formattedDate() {
      if (!this.submission.created_at) return ''
      return new Date(this.submission.created_at).toLocaleDateString('ru-RU')
    }
  }
}
</script>>

<style scoped>
.movie-suggestion-card {
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.movie-suggestion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.card-content{
  display: flex;
  flex-direction: column;
  color: white;
  border-color: gray;
  border-width: 0.1rem;
  border-style: dotted;
  width: 82vw;
  height: fit-content;
  padding: 0.1rem;
}

.movie-title {
  font-family: "Blackout Two AM";
  overflow-wrap: break-word;
  flex-grow: 2;
  text-overflow: ellipsis;
  font-size: 1.3rem;
}

.movie-description {
  padding: 0.2rem;
  overflow-wrap: break-word;
  text-overflow: ellipsis;
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
    display: flex;
    flex-direction: row;
    box-sizing:border-box;
    width: 100vw;
    margin-left: -50vw;
    position: relative;
    left: 50%;
    gap: 0.5rem;
  }
  
  .movie-title {
    font-size: 1.3rem;
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
    font-size: 1.3rem;
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