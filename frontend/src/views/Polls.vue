<template>
  <div class="page-header">
    <router-link to="/" class="back-button">← BACK</router-link>
    <div class="layout">
        <div class="page-signal">
          <span class="header-text">PICK A POLL</span>
          <span class="header-text2">TO VOTE</span>
        </div>  
        <p class="info-text">Pick an active poll or look through previous ones</p>
        
        
        

        <NewPollButton />




        <div class="suggestions-section">
      <h2>submissions</h2>
      <div v-if="loading" class="loading">LOADING...</div>
      <div v-else-if="error" class="error">
        {{ error }}
        <button @click="fetchPolls" class="btn btn-secondary">TRY AGAIN</button>
      </div>
      <div v-else-if="polls.length === 0" class="empty">NO POLLS</div>
      <div v-else class="poll-list">
        <PollUnit 
          v-for="poll in polls" 
          :key="poll.id"
          :poll="polls"
          @click="viewPolls(poll.id)"
        />
      </div>
    </div>
      
    </div>
</div>   
</template>

<script>
import PollUnit from '@/components/PollUnit.vue';
import NewPollButton from '@/components/NewPollButton.vue';
export default {
  name: 'Polls',
  components: {
    PollUnit,
    NewPollButton
  },
  data() {
    return {
      polls: [],
      loading: false,
      error: null,
    }
  },
  async mounted() {
    await this.fetchPolls()
  },
  methods: {
    async fetchPolls() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch('http://localhost:8000/polls')
        if (response.ok) {
          this.polls = await response.json()
          console.log('Loaded polls:', this.polls) // Для отладки
        } else {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
      } catch (error) {
        console.error('Error loading polls:', error)
        this.error = 'Mistake when loading the movie list: ' + error.message
      } finally {
        this.loading = false
      }
    },
    viewPolls(id) {
      this.$router.push(`/polls/${poll_id}`)
    }
  },
}
</script>

<style>

.text{
color: gray;
font-size: 12px;
position: center;
}
.back-button {
  padding-bottom: 30px;
  color:#0f6f62;
}

.page-header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-top: 2cap;
}
.poll-title {
  color: rgba(149, 91, 153, 1);
}

.poll-status {
  color: rgb(0, 0, 0);
  padding-bottom: 1cap;
}
.title {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.layout {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
}

span {
  display: inline-block;
  padding: 5px;
}

.poll-box {
    display: flex;
    flex-direction: column;
    background-color: azure;
    padding: 1rem;
}

.header-text {
    color:rgba(244, 233, 172, 1) ;
    inset-inline: auto;
    font-size: 23px
}

.header-text2 {
    color:rgba(149, 91, 153, 1);
    inset-inline: auto;
    font-size: 24px
}

.info-text {
    color:rgba(244, 233, 172, 1) ;
    text-align: center;
    
}

.page-signal{
  margin: auto;
}
</style>