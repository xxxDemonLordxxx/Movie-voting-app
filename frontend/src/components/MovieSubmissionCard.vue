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

    <div class="btn-block">
     <img src='@/assets/more_button.png' @click="viewSubmission(submission.id)" class="more-button" />
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
      return new Date(this.submission.created_at).toLocaleDateString('en-EN')
    }
  },
    methods: {
    viewSubmission(id) {
      this.$router.push(`/submissions/${id}`)
    }
  }
}

</script>>

<style scoped>
.movie-suggestion-card {
  display: flex;
  flex-direction: row;
  box-sizing:border-box;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  height: 13rem;
  margin:1rem
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
  width: 200%;
  padding: 0.1rem;
  box-sizing:border-box;
  overflow:hidden;
}

.movie-title {
  font-family: "Blackout Two AM";
  flex-grow: 1;
  font-size: 1.3rem;
  overflow-wrap: break-word;
  text-overflow:ellipsis;
  overflow: clip;
  box-sizing:border-box;
  white-space: nowrap;
}

.movie-description {
  padding: 0.2rem;
  overflow-wrap: break-all;
  text-overflow:ellipsis;
  overflow: clip;
  box-sizing:border-box;
  flex-grow: 2;
  
}

.suggestion-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #7f8c8d;
  border-top: dotted 1px;
  border-color: gray;
  line-height: 1
}

.suggester {
  font-weight: 500;
}

.date {
  color: #95a5a6;
}

.btn-block{
  display: flex;
  flex-direction: row;
  color: white;
  border-color: gray;
  border-width: 0.1rem;
  border-style: dotted;
  flex-shrink:2;
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
    font-size: 1rem;
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
  }
  
  .movie-description {
    font-size: 0.85rem;
    margin-bottom: 0.75rem;
  }
  
  .suggestion-info {
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