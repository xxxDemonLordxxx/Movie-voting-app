<template>
  <FringeHeader v-if="pollInfo" :pollInfo="pollInfo" />

    <OfferPopup 
    psa="in da club, we appreciate enthusiasm, 
    so so that you can vote and mayhaps get your movie 
    in da club. its not that deep but please do 
    consider and try to pick something that is 
    really really cool and get a pitch to really really"
    haha="haha"
    psa2="sell it. click haha if ya ready for democratic experience"
    />
    
    <form @submit.prevent="submitSubmission" class="form">
      <div class="name-group">
        <label for="author">YOUR NAME:</label>
        <div class="checkbox">
          <label class="checkbox-label">   
            <input
              type="checkbox"
              v-model="form.isAnonymous"
              class="checkbox"
            />ANONYMUS</label>
        </div>
      </div>
        <div class="form-group" 
        :class="{ 'disabled-style': form.isAnonymous }"
        >
          <p class="search-pretty" 
          :class="{ 'disabled-style': form.isAnonymous }"
          >(</p>

          <input
            id="author"
            v-model="form.author"
            :disabled="form.isAnonymous"
            placeholder="write your name"
            class="form-input"
          />
          <p class="search-pretty" 
          :class="{ 'disabled-style': form.isAnonymous }"
          >)</p>
        </div>


      <label for="movieTitle">TITLE:</label>
      <div class="form-group">
        <p class="search-pretty">(</p>
        <TMDB
          id="movieTitle"
          v-model="form.movieTitle"
          placeholder="enter the film title"
          required
          class="form-input"
        />
        <p class="search-pretty">)</p>
      </div>

      <label for="movieDescription">COMMENT:</label>
      <div class="form-group long-input">
        
        <p class="search-pretty prcomment">(</p>
        <textarea
          id="movieDescription"
          v-model="form.movieDescription"
          placeholder="enter your own pitch or film description"
          required
          rows="4"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty prcomment">)</p>
      </div>
      
      <div class="form-actions">
        <button type="submit" :disabled="submitting" class="btn btn-primary">
          {{ submitting ? 'Sending...' : 'DONE' }}
        </button>
      </div>
    </form>
</template>

<script>
import TMDB from '@/components/TMDBsearch.vue'
import OfferPopup from '@/components/OfferPopup.vue';
import FringeHeader from '@/components/FringeHeader.vue';
export default {
  name: 'SubmissionForm',
  components: {
    TMDB,
    OfferPopup,
    FringeHeader
  },
  
  data() {
    return {
      submissions: [],
      pollInfo: null,
      loading: false,
      error: null,
      form: {
        author: '',
        isAnonymous: false,
        movieTitle: '',
        movieDescription: ''
      },
      submitting: false
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
    async submitSubmission() {
      if (!this.form.movieTitle.trim() || !this.form.movieDescription.trim()) {
        alert('PLEASE, FILL ALL')
        return
      }

      this.submitting = true
      
      try {
        const response = await fetch('http://localhost:8000/submissions/new', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            poll_id: parseInt(this.$route.params.id),
            author: this.form.isAnonymous ? null : this.form.author,
            comment: this.form.movieDescription,
            image_Url: null,
            movie: {
              tmdb_id: null,
              title: this.form.movieTitle,
              language: "en-US"            
            }
          })
        })

        if (response.ok) {
          alert('FILM SUBMITTED')
          this.resetForm()
          this.$router.push(`/polls/${this.$route.params.id}`)
        } else {
          throw new Error('SENDING ERROR')
        }
      } catch (error) {
        console.error('Error:', error)
        alert('SENDING ERROR при отправке предложения')
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.form = {
        author: '',
        isAnonymous: false,
        movieTitle: '',
        movieDescription: ''
      }
    }
  }
}

</script>

<style scoped>


.submission-form h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.submission-form  {
  min-width: 324px;
  align-self: center;
}


.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: white;
  align-items: center;
  line-height: 1.2;
  padding: 0rem;
}

.name-group {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-bottom: 0.2rem;
}

.long-input {
  align-items: baseline;
}

label {
  display: block;
  color: #ffffff;
  background-color: none;
}

.form-input,
.form-textarea {
  
  width: 100%;
  border: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: rgb(82, 39, 85);

}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-input:disabled,
.disabled-style {
  background-color: #645757;
  color: #999;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox {
  width: auto;
  padding-right: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}




.poll-title {
  color: rgb(166, 111, 170);

}

.page-title {
  color:rgb(255, 255, 255);
  text-align: center;
}



span {
  display: inline-block;
  padding: 5px;
}

.prcomment{
  align-self: end;
}



/* Мобильные стили */
@media (max-width: 768px) {
  .submission-form h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  label {
    font-size: 0.9rem;
  }
  
  .form-input,
  .form-textarea {
    padding: 0.2rem;
    font-size: 14px;
  }
  
  .btn {
    padding: 8px 16px;
    font-size: 14px;
  }
  
  .form-actions {
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .submission-form h1 {
    font-size: 1.3rem;
  }

  
  .form-group {
    margin-bottom: 0.3rem;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .btn {
    width: 100%;
    padding: 10px;
  }
  
  .checkbox-label {
    font-size: 0.9rem;
  }
}
</style>