<template>
  <div class="page-header">
    <div class="adminheader">
      <router-link to="/" class="back-button">← BACK</router-link>
      <div class="NewPollButton">
        <NewPollButton />
      </div>
    </div>
    <div class="layout">
        <div class="view-header">
            <div class="page-signal">
              <span class="header-text">PICK A POLL TO</span>
              <span class="header-text special">VOTE</span>
            </div>  
            <p class="info-text">or look through previous ones</p>
        </div>
        
        
        
        <div class="suggestions-section">
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
          :poll="poll"
          @click="viewSubmissionList(poll.id)"
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
      form: {
        pollTitle: '',
        pollEnd: '',
      },
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
          console.log('Loaded polls:', this.poll) // Для отладки
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
    viewSubmissionList(id) {
      this.$router.push(`/polls/${id}`)
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
  padding-bottom: 0px;
  color:#0f6f62;
}

.view-header {
  display: flex;
  flex-direction: column;
  padding-bottom: 1rem;
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

.poll-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.header-text {
    color:rgba(244, 233, 172, 1) ;
    inset-inline: auto;
    font-size: 23px;

}

.special {
    color:#61b0a8;
    font-family: "Blackout Two AM";
}

.info-text {
    color:rgba(244, 233, 172, 1) ;
    text-align: center;
}


.adminheader{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.poll-box:hover {
    background-color: hwb(160 58% 25%);
    transition: 0.4s;
    }
</style>