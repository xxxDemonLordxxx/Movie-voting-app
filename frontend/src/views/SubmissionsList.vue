<template> 
  <div class="submissions-section">
    <router-link to="/polls" class="back-button">← BACK TO THE LIST</router-link>
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
          v-for="(submission,index) in submissions" 
          :key="submission.id || index "
          :submission="submission"
          class="submission"
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
    }
  },

  computed: {
    pollId() {
      const id = this.$route.params.id;
      console.log('Computed pollId from route:', id);
      return parseInt(id) || null;
    }
  },
  async mounted() {
    console.log('Mounted - pollId computed:', this.pollId);
    if (this.pollId) {
      await this.fetchSubmissions();
    } else {
      this.error = 'No valid poll ID found';
    }
  },

  methods: {
    async fetchSubmissions() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch(`http://localhost:8000/polls/${this.pollId}`)
        if (response.ok) {
          this.submissions = await response.json()
          console.log('Loaded submissions:', this.submissions) // Для отладки
        } else {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
      } catch (error) {
        console.error('Error loading submissions:', error)
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
.calendar-title {
  color: white;
  position: center;
}

.submission {
  padding-top: 2rem;
  display: flex;
  flex-direction: row;
}

</style>