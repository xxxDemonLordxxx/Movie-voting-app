<template>
  <div class="suggestion-form">
    <div class="page-header">
      <router-link to="/" class="back-button">← BACK</router-link>
      <div class="title">
        <span class="poll-title">DECEMBER</span> 
        <span class="page-title">POLL</span>
      </div>
    </div>
    <p class="page-title">HERE YOU CAN OFFER YR OWN PICK</p>
    <form @submit.prevent="submitSuggestion" class="form">
      <div class="form-group">
        <label for="suggesterName">YOUR NAME:</label>
        <input
          id="suggesterName"
          v-model="form.suggesterName"
          :disabled="form.isAnonymous"
          placeholder="Write your name"
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label class="checkbox-label">
          <input
            type="checkbox"
            v-model="form.isAnonymous"
            class="checkbox"
          />
          Anonymus
        </label>
      </div>
      
      <div class="form-group">
        <label for="movieTitle">TITLE:</label>
        <input
          id="movieTitle"
          v-model="form.movieTitle"
          placeholder="Enter the film title"
          required
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label for="movieDescription">FILM DESCRIPTION OR YOUR OWN PITCH:</label>
        <textarea
          id="movieDescription"
          v-model="form.movieDescription"
          placeholder="Enter the text"
          required
          rows="4"
          class="form-textarea"
        ></textarea>
      </div>
      
      <div class="form-actions">
        <button type="submit" :disabled="submitting" class="btn btn-primary">
          {{ submitting ? 'Sending...' : 'DONE' }}
        </button>
        <router-link to="/" class="btn btn-secondary">BACK</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SuggestionForm',
  data() {
    return {
      form: {
        suggesterName: '',
        isAnonymous: false,
        movieTitle: '',
        movieDescription: ''
      },
      submitting: false
    }
  },
  methods: {
    async submitSuggestion() {
      if (!this.form.movieTitle.trim() || !this.form.movieDescription.trim()) {
        alert('PLEASE, FILL ALL')
        return
      }

      this.submitting = true
      
      try {
        const response = await fetch('http://localhost:8000/suggestions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            suggester_name: this.form.isAnonymous ? null : this.form.suggesterName,
            is_anonymous: this.form.isAnonymous,
            title: this.form.movieTitle,
            description: this.form.movieDescription
          })
        })

        if (response.ok) {
          alert('FILM SUBMITTED')
          this.resetForm()
          this.$router.push('/')
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
        suggesterName: '',
        isAnonymous: false,
        movieTitle: '',
        movieDescription: ''
      }
    }
  }
}

</script>

<style scoped>
.suggestion-form {
  max-width: 600px;
  margin: 0 auto;
}

.suggestion-form h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form {
  background: white;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #333;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 5px;
  border: 1px solid #ddd;
  font-size: 16px;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-input:disabled {
  background-color: #f5f5f5;
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
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #065f53;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0f6f62;
}

.btn-primary:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.back-button {
  padding-bottom: 30px;
  color:#0f6f62;
}

.page-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-top: 2cap;
}
.poll-title {
  color: rgba(149, 91, 153, 1);
}

.page-title {
  color: aliceblue;
  padding-bottom: 1cap;
}
.title {
  inset-inline: auto;
  
}

span {
  display: inline-block;
  padding: 5px;
}


/* Мобильные стили */
@media (max-width: 768px) {
  .suggestion-form h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .form {
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  label {
    font-size: 0.9rem;
  }
  
  .form-input,
  .form-textarea {
    padding: 8px;
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
  .suggestion-form h1 {
    font-size: 1.3rem;
  }
  
  .form {
    padding: 1rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
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