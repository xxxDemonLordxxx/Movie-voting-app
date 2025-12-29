<template>
  <FringeHeader v-if="pollInfo" :pollInfo="pollInfo" :submissions="submissions"/>
    
    <OfferPopup 
    psa="it takes great balance between 
    democracy and leadership to carry the
    boat forward. This site is not made to stop
    you from voting more than once. However, we,"
    haha="humble servants,"
    psa2="do these polls
    to make sure most people will be interested
    in coming to the screening. So please, abstain
    from cheating. Click humble servants to continue to polls"
    />


  

      <div class="form-section">
        <VotingInput
          v-model="voteData"
          :submissions="submissions"
          :pollInfo="pollInfo"
          @view-submission="viewSubmission"
          ref="votingInput"
        />
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <button @click="submitVote" class="btn">
          Submit Vote
        </button>
        <button @click="clearVote" class="btn">
          Clear All
        </button>
      </div>
    
    <div v-if="isAdmin">
      <VoteStatusbtn
      statusChange="stop"
      ></VoteStatusbtn>
    </div>
</template>


<script>
import FringeHeader from '@/components/FringeHeader.vue';
import OfferPopup from '@/components/OfferPopup.vue';
import VotingInput from '@/components/VotingInput.vue';
import VoteStatusbtn from '@/components/VoteStatusbtn.vue';
export default {
  name: 'VotingForm',
  components: {
    OfferPopup,
    FringeHeader,
    VotingInput,
    VoteStatusbtn
  },
  data() {
    return {
      submissions: [],
      pollInfo: null,
      loading: false,
      error: null,
      voteData: '', // Comma-separated string of IDs
      isAdmin: false
    }
  },

  computed: {
    pollId() {
      const id = this.$route.params.id;
      console.log('Computed pollId from route:', id);
      return parseInt(id) || null;
    }
  },



   parsedVoteData() {
    // Check if voteData exists and is a string
    if (!this.voteData || typeof this.voteData !== 'string') {
      return [];
    }
    
    // Split and process
    const ids = this.voteData.split(',');
    const result = [];
    
    for (let i = 0; i < ids.length; i++) {
      const id = ids[i].trim();
      if (!id) continue; // Skip empty strings
      
      const submission = this.submissions.find(s => {
        if (!s || !s.id) return false;
        return s.id.toString() === id;
      });
      
      result.push({
        id: id,
        title: submission?.movie?.title || submission?.title || 'Unknown Movie',
        position: i + 1
      });
    }
    
    return result;
  },



  async mounted() {
    await this.fetchSubmissions(), this.checkAdmin();
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
      
    async checkAdmin() {
      const storedAdmin = localStorage.getItem('isAdmin')
      this.isAdmin = storedAdmin === 'true'
    },

    async submitVote() {
  // Get data directly from VotingInput component
  const votingInput = this.$refs.votingInput;
  
  if (!votingInput) {
    alert('Form error. Please refresh the page.');
    return;
  }
  
  // Get selected submissions directly
  const selectedSubmissions = votingInput.selectedSubmissions || [];
  const validSelections = selectedSubmissions.filter(sub => sub && sub.id);
  
  if (validSelections.length === 0) {
    alert('Please select at least one movie for voting.');
    return;
  }
  
  // Create comma-separated string
  const voteData = validSelections.map(sub => sub.id).join(',');
  
  // Create ranked submissions array
  const rankedSubmissions = validSelections.map((sub, index) => ({
    submission_id: sub.id,
    rank: index + 1
  }));
  
  console.log('Submitting vote with data:', {
    voteData,
    rankedSubmissions
  });
  
  const votePayload = {
    poll_id: this.pollId,
    rankings: validSelections.map(sub => sub.id), // Array of strings
  };
      
      try {
        // Replace with your actual API endpoint
        const response = await fetch('http://localhost:8000/polls/vote', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(votePayload)
        });
        
        if (response.ok) {
          const result = await response.json();
          alert('Vote submitted successfully!');
          // Redirect or show success message
          this.$router.push(`/polls/${this.pollId}`);
        } else {
          throw new Error('Failed to submit vote');
        }
      } catch (error) {
        console.error('Error submitting vote:', error);
        alert('Error submitting vote. Please try again.');
      }
    },
    
    clearVote() {
      this.voteData = '';
      // If you need to clear the component's internal state
      if (this.$refs.votingInput) {
        this.$refs.votingInput.parseInitialValue('');
      }
    },


    viewSubmission(id) {
      this.$router.push(`/submissions/${id}`)
    }
  },
}
</script>


<style>
.text{
color: white;
font-size: 16px;
position: center;
}

.back-button {
  padding-bottom: 30px;
  color:#0f6f62;
}

.page-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-top: 2rem;
}
.poll-title {
  color: rgba(149, 91, 153, 1);
  text-align: center;
}

.page-title {
  color: aliceblue;
  padding-bottom: 1cap;
}
.title {
  text-align: center;
}

span {
  display: inline-block;
  padding: 5px;
}

.input-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: white;
  align-items: center;
  line-height: 1.2
}

.form-input,
.form-textarea {
  width: 100%;
  border: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: rgb(82, 39, 85);
}

.number {
  color: black;
  padding: 0.3rem;
}

.search-pretty {
  color: rgba(149, 91, 153, 1);
  font-size: 1.50rem;
  font-weight: 350;
  font-family:Verdana, Geneva, Tahoma, sans-serif;
  padding-left: 0.3rem;
  padding-right: 0.3rem;
}
</style>