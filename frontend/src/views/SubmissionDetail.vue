<template>
  <div class="submission-detail">
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="submission" class="detail-content">
      <div class="back-button">
        <button @click="$router.go(-1)" class="btn btn-secondary">← BACK TO THE LIST</button>
      </div>
      
      <MovieDetailCard :submission="submission" />
    </div>
    <div v-else class="error">Предложение не найдено</div>
  </div>
</template>

<script>
import MovieDetailCard from '@/components/MovieDetailCard.vue'

export default {
  name: 'SubmissionDetail',
  components: {
    MovieDetailCard
  },
  data() {
    return {
      submission: null,
      loading: false
    }
  },
  async mounted() {
    await this.fetchSubmissionDetail()
  },
  methods: {
    async fetchSubmissionDetail() {
      this.loading = true
      try {
        const response = await fetch(`http://observational.website/submissions/${this.$route.params.id}`)
        if (response.ok) {
          this.submission = await response.json()
        } else if (response.status === 404) {
          this.submission = null
        }
      } catch (error) {
        console.error('Error:', error)
        alert('Ошибка при загрузке данных о предложении')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.submission-detail {
  max-width: 600px;
  margin: 0 auto;
}

.btn-secondary {
  margin-bottom: 2rem;
  color:#0f7f70;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

/* Мобильные стили */
@media (max-width: 768px) {
  .back-button {
    margin-bottom: 1.5rem;
  }
  
  .btn {
    padding: 8px 16px;
    font-size: 14px;
  }
  
  .loading, .error {
    padding: 1.5rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .back-button {
    margin-bottom: 1rem;
  }
  
  .btn {
    width: 100%;
    text-align: center;
  }
}
</style>