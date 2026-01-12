<template> 
    
  <FringeHeader v-if="pollInfo" :pollInfo="pollInfo" :submissions="submissions"/>
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
          v-for="(submission,index) in submissions" 
          :key="submission.id || index "
          :submission="submission"
          class="submission"
          @show-dialog="showDialog"
        />
      </div>
      <MovieDetailCard 
      ref="dialogRef" 
      :submission="selectedSubmission"
      v-if="selectedSubmission"
      />
    </div>

 
</template>

<script>
import FringeHeader from '@/components/FringeHeader.vue';
import MovieDetailCard from '@/components/MovieDetailCard.vue';
import MovieSubmissionCard from '@/components/MovieSubmissionCard.vue'
export default {
  name: 'SubmissionsList',
  components: {
    MovieSubmissionCard,
    FringeHeader,
    MovieDetailCard
  },
  data() {
    return {
      submissions: [],
      submission: null,
      pollInfo: null,
      loading: false,
      error: null,
      selectedSubmission: null
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
          const data = await response.json()  // Get the full response
          
            // Extract both poll info and submissions
            this.pollInfo = data.poll_info      // This was missing!
            this.submissions = data.submissions // This needs to be from data.submissions
            
            console.log('Loaded poll info:', this.pollInfo)
            console.log('Loaded submissions:', this.submissions)
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
    showDialog(submission) {
      this.selectedSubmission = submission
      this.$nextTick(() => {
        this.$refs.dialogRef?.showModal()
      })
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