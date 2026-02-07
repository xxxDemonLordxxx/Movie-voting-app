<template>
  <div class="page-header">
    <div class="adminheader">
      <router-link to="/" class="back-button">← BACK</router-link>
      <div v-if="isAdmin" class="NewEventButton">
        <NewPollButton />
      </div>
    </div>
    <div class="layout">
        <div class="view-header">
            <div class="page-signal">
              <span class="header-text">PICK A POLL TO</span>
              <span class="header-text special">VOTE</span>
              <span class="header-text">OR</span>
              <span class="header-text special">OFFER</span>
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
          @click="viewSubmissionList(poll.id, poll.state_name)"
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
      isAdmin: false
    
    }
  },

  async mounted() {
    await this.fetchPolls(), this.checkAdmin();
  },
  methods: {
    async fetchPolls() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch('http://observational.website/polls')
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
    checkAdmin() {
      const storedAdmin = localStorage.getItem('isAdmin')
      this.isAdmin = storedAdmin === 'true'
    },
        viewSubmissionList(id, stateName) {
      if (stateName === 'offer') {
        this.$router.push(`/submissions/new/${id}`)
      } else if (stateName === 'vote') {
        this.$router.push(`/voting/${id}`)
      } else if (stateName === 'previous') {
        this.$router.push(`/polls/${id}`)
      } 
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
  padding-bottom: 1rem;
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

.page-signal{
  text-align: center;
}
.header-text {
    color:rgba(244, 233, 172, 1) ;
    inset-inline: auto;
    font-size: 1.2rem;

}

.special {
    color:#1a584a;
    font-family: "Blackout Two AM";
    background-color: rgba(244, 233, 172, 1);
    padding: 2px;
}

.info-text {
    color:rgba(244, 233, 172, 1) ;
    text-align: center;
    font-size: 0.8rem;
    margin: 0 1.5rem 2rem 1.5rem
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