<template>
  <FringeHeader v-if="pollInfo" :pollInfo="pollInfo" />
    
    <OfferPopup 
    psa="it takes great balance between 
    democracy and leadership to carry the
    boat forward. This site is not made to stop
    you from voting more than once. However, we,"
    haha="humble servants"
    psa2="do these poll
    to make sure most people will be interested
    in coming to the screening. So please, abstain
    from cheating. Click humble servants to continue to polls"
    />

    <form>
      <div class="input-group">
        <p class="number">1</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

      <div class="input-group">
        <p class="number">2</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

      <div class="input-group">
        <p class="number">3</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

      <div class="input-group">
        <p class="number">4</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

    </form>
    

</template>


<script>
import FringeHeader from '@/components/FringeHeader.vue';
import OfferPopup from '@/components/OfferPopup.vue';
export default {
  name: 'VotingForm',
  components: {
    OfferPopup,
    FringeHeader
  },
  data() {
    return {
      submissions: [],
      pollInfo: null,
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
    viewSubmission(id) {
      this.$router.push(`/submissions/${id}`)
    }
  }
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