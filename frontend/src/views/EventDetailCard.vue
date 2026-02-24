<template>
  <div class="back-button">
        <button @click="$router.go(-1)" class="btn btn-secondary">← BACK TO THE LIST</button>
      </div>
  <div class="container">
      <div class="movie-detail-card">
        <div class="card-header">
          <h1 class="movie-title">{{ eventTitle }}</h1>
        </div>
    
    <div class="card-body">
      <div class="description-section">
        <h3>description:</h3>
        <p class="movie-description">{{ eventDescription }}</p>
      </div>
      
        <div class="submission-meta">
        <div class="meta-item">
          <strong>time:</strong>
          <span>{{eventTime }}</span>
        </div>
        
        <div class="meta-item">
          <strong>date:</strong><span>{{ eventDate }}</span>
        </div>

          <pre>{{ JSON.stringify(event, null, 2) }}</pre>
        </div>

        </div>
      </div>
  </div>
</template>



<script>
export default {
  name: 'EventDetailCard',
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  data(){
    return {
      dialogElement: null
    }
  },
  data() {
    return {
      event: null,
      loading: false
    }
  },
  async mounted() {
    await this.fetchEventDetail()
  },
  methods: {
    async fetchEventDetail() {
      this.loading = true
      try {
        const response = await fetch(`api/events/${this.$route.params.id}`)
        if (response.ok) {
          this.event = await response.json()
        } else if (response.status === 404) {
          this.event = null
        }
      } catch (error) {
        console.error('Error:', error)
        alert('Ошибка при загрузке данных о предложении')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>

.hidden-content {
  display: none;
}

.dialog {
  background-color: rgb(24, 23, 25);;
  width: 95vw;
  
  overflow: scroll;
}

.dialog[open] {
  display: block;
  margin: auto;
  width: 100%;
}

.movie-detail-card {
  border-color: gray;
  border-width: 0.1rem;
  border-style: dotted;
  overflow: hidden;
  color: white;
}

.card-header {
  padding: 2rem;
  font-family: "Blackout Two AM";
}

.movie-title {
  margin: 0;
  font-size: 2rem;
  text-align: center;
  color: white;
  word-break: break-word;
}

.card-body {
  padding: 2rem;
  color: white;
}

.description-section {
  margin-bottom: 2rem;
}

.description-section h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.movie-description {
  line-height: 1.6;
  font-size: 1.1rem;
  word-break: break-word;
}

.submission-meta {
  border-top: 1px solid #ffffff;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #ffffff;
}

.meta-item:last-child {
  border-bottom: none;
}


.status-badge {
  background: #ffeaa7;
  color: #e17055;
  padding: 4px 12px;
  font-size: 0.9rem;
  font-weight: 500;
}

.btn {
  padding: 4px 12px;
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
  padding: 4px 12px
}
.btn-primary:hover:not(:disabled) {
  background-color: #0f6f62;
}

.text {
  padding: 0.75rem 0;
  gap: 0.25rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

/* Мобильные стили */
@media (max-width: 768px) {
  .card-header {
    padding: 1.5rem;
  }
  
  .movie-title {
    font-size: 1.5rem;
  }
  
  .card-body {
    padding: 1.5rem;
  }
  
  .description-section h3 {
    font-size: 1.2rem;
  }
  
  .movie-description {
    font-size: 1rem;
    line-height: 1.5;
  }
  
  
  .meta-item {
    padding: 0.6rem 0;
  }
}

@media (max-width: 480px) {
  .card-header {
    padding: 1rem;
  }
  
  .movie-title {
    font-size: 1.3rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .description-section {
    margin-bottom: 1.5rem;
  }
  
  .description-section h3 {
    font-size: 1.1rem;
  }
  
  .movie-description {
    font-size: 0.95rem;
  }
  
  .meta-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .status-badge {
    font-size: 0.8rem;
    padding: 3px 8px;
  }
}
</style>