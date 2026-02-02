<template>
  <FringeHeader v-if="pollInfo" :pollInfo="pollInfo" :submissions="submissions" />

    <OfferPopup 
    psa="in da club, we appreciate enthusiasm, 
    so so that you can vote and mayhaps get your movie 
    in da club. its not that deep but please do 
    consider and try to pick something that is 
    really really cool and get a pitch to really really"
    haha="haha"
    psa2="sell it. click haha if ya ready for democratic experience. 
    TIP -
    if you want to add something to someone else's pitch just offer the same movie again
    with your own addition comment
    
    
    TIP 2 - tick copy checkbox to share the pitch with out group"
    />
    
    <form @submit.prevent="submitSubmission" class="form">

        <label for="author">YOUR NAME:</label>
        <div class="form-group" 
        :class="{ 'disabled-style': form.isAnonymous }"
        >
          <p class="search-pretty" 
          :class="{ 'disabled-style': form.isAnonymous }"
          >(</p>

          <input
            id="author"
            v-model="form.author"
            :class="{ 'disabled-style': form.isAnonymous }"
            :placeholder="form.isAnonymous ? 'anonymus for now' : 'write your name'"
            class="form-input"
          />

          <p class="search-pretty pretty-anon" 
          :class="{ 'disabled-style': form.isAnonymous }"
          >)</p>

          <button 
            v-if="!form.isAnonymous"
            @click="makeAnonymous"
            class="clear-position-btn"
          >
            <img 
            src='@/assets/anonglaz.svg' 
            class="anonbtn"
             />
          </button>
          
        </div>

        

      <label for="movieTitle">TITLE:</label>
      <div class="form-group">
        <p class="search-pretty">(</p>
        <input
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
        <div class="split-button-container" :class="{ 'copied': isCopied }">
          <button 
            type="button"
            class="copy-btn"
            :class="{ 'active': isCopied, 'copied': isCopied }"
            @click="toggleCopy"
            :disabled="submitting"
          >
            <span v-if="!isCopied" class="copy-text">COPY</span>
            <span v-else class="checkmark">🗸</span>
          </button>

          <button 
            type="submit"
            :disabled="submitting"
            class="submit-btn"
            :class="{ 'copied': isCopied }"
          >
            {{ submitting ? 'Sending...' : 'DONE' }}
          </button>
        </div>
      </div>
    </form>

    <VoteStatusbtn
    statusChange="start"
    v-if="isAdmin"
    >start voting</VoteStatusbtn>
</template>

<script>
import TMDB from '@/components/TMDBsearch.vue'
import OfferPopup from '@/components/OfferPopup.vue';
import FringeHeader from '@/components/FringeHeader.vue';
import VoteStatusbtn from '@/components/VoteStatusbtn.vue';
export default {
  name: 'SubmissionForm',
  components: {
    TMDB,
    OfferPopup,
    FringeHeader,
    VoteStatusbtn
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
      submitting: false,
      isAdmin: false,
      isCopied: false,
      autoCopy: false,
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
      await this.fetchSubmissions(), this.checkAdmin();
    } ,

  methods: {
    toggleCopy() {
      if (!this.isCopied) {
        // Copy to clipboard
        const text = `${this.form.movieTitle}\n\npitch:\n${this.form.movieDescription}\n\n`;
        navigator.clipboard.writeText(text)
          .then(() => {
            this.isCopied = true;
            this.autoCopy = true;
          })
          .catch(err => {
            console.error('Failed to copy: ', err);
            alert('Failed to copy to clipboard');
          });
      } else {
        // Un-copy (reset)
        this.isCopied = false;
        this.autoCopy = false;
      }
    },
     makeAnonymous() {
      this.form.isAnonymous = true;
      this.form.author = '';
    },
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
      checkAdmin() {
      const storedAdmin = localStorage.getItem('isAdmin')
      this.isAdmin = storedAdmin === 'true'
    },
    async submitSubmission() {
      if (!this.form.movieTitle.trim() || !this.form.movieDescription.trim()) {
        alert('PLEASE, FILL ALL')
        return
      }
      if (this.autoCopy) {
        const text = `${this.form.movieTitle}\n\npitch:\n${this.form.movieDescription}\n\n`;
        navigator.clipboard.writeText(text);
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
  },
  watch: {
    'form.author': function(newVal) {
      if (newVal.trim() !== '') {
        this.form.isAnonymous = false;
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
  background-color: #0c2925;
  color: rgb(19, 140, 120);
}
.clear-position-btn {
  padding: 0.1rem 0.2rem;
  background: none;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  transition: all 0.3s ease;
}



.anonbtn{
  margin-bottom: -0.2rem;
  height: 1.5rem;
  color: #522755;
  animation: popIn 0.3s ease;
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
  justify-content: center;
  margin-top: 1.5rem;
}
.split-button-container {
  display: flex;
  height: 2rem;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}


.copy-btn {
  flex: 1;
  background: none;
  border: 3px dotted #006655;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  color: #065f53;
  
}


.copy-btn.active {
  flex: 0 0 2rem;
  color: #065;
  background-color: rgba(149, 91, 153, 1);
  border: none;
}



.copy-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  
}

.submit-btn {
  flex: 1;
  background: #065f53;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #06312c;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn.copied {
  flex: calc(1 + 0.5); /* Takes up more space when copy is active */
}

/* Animation for the checkmark */
.checkmark {
  font-size: 1.5rem;
  animation: popIn 0.3s ease;
  filter: drop-shadow(0.05rem 0.1rem 0.2rem  rgb(255, 36, 91));
  font-weight: 600;
}

@keyframes popIn {
  0% {
    transform: scale(0);
  }
  70% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

/* Tooltip for copy button */
.copy-btn {
  position: relative;
}

.copy-btn::after {
  content: 'Click to copy, click again to reset';
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  margin-bottom: 8px;
  z-index: 100;
}

.copy-btn:hover:not(:disabled):not(.active)::after {
  opacity: 1;
}

.copy-btn.active::after {
  content: 'Click to reset';
}

.copy-btn.active:hover::after {
  opacity: 1;
}
.prcomment{
  align-self: end;
}

.pretty-anon{
  margin-right: -0.3rem;
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