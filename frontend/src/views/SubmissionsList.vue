<template> 
  <div class="submissions-section">
      <div v-if="loading" class="loading">LOADING...</div>
      <div v-else-if="error" class="error">
        {{ error }}
        <button @click="fetchSubmissions" class="btn btn-secondary">TRY AGAIN</button>
      </div>
      <div v-else-if="submissions.length === 0" class="empty">
        NO SUBMISSIONS YET
      </div>
      <div v-else class="submissions-list">
        <MovieSubmissionCard 
          v-for="submission in submissions" 
          :key="submission.id"
          :submission="submission"
          @click="viewSubmission(submission.id)"
        />
      </div>
    </div>
</template>

<script>
import MovieSubmissionCard from '@/components/MovieSubmissionCard.vue'

export default {
  name: 'SubmissionsList',
  components: {
    MovieSubmissionCard
  },
  data() {
    return {
      submissions: [],
      loading: false,
      error: null,
      form: {
        movieTitle: '',
        truncatedComment: '',
        author: '',
        formattedDate: '',
      },
    }
  },
  async mounted() {
    await this.fetchSubmissions()
  },
  methods: {
    async fetchSubmissions() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch('http://localhost:8000/polls/')
        if (response.ok) {
          this.submissions = await response.json()
          console.log('Loaded submissions:', this.submissions) // Для отладки
        } else {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
      } catch (error) {
        console.error('Error loading suggestions:', error)
        this.error = 'Mistake when loading the movie list: ' + error.message
      } finally {
        this.loading = false
      }
    },
    viewSubmission(id) {
      this.$router.push(`/submissions/${id}`)
    }
  }
}

</script>

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
}

.calendar-title {
  color: white;
  position: center;
}

.submission {
  padding-top: 2cap;
  display: flex;
  flex-direction: row;
}

</style>