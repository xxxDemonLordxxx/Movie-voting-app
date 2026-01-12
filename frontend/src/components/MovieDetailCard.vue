<template>
  <div class="container">

    <dialog class="dialog" ref="dialog">
    <button  
      type="button" 
      aria-label="close"
      @click="closeDialog"
      class="close-btn"
    >x</button>

    
      <div class="movie-detail-card">
        <div class="card-header">
          <h1 class="movie-title">{{ movieTitle }}</h1>
        </div>
    
    <div class="card-body">
      <div class="description-section">
        <h3>pitch:</h3>
        <p class="movie-description">{{ comment }}</p>
      </div>
      
        <div class="submission-meta">
        <div class="meta-item">
          <strong>offered by:</strong>
          <span>{{ author }}</span>
        </div>
        
        <div class="meta-item">
          <strong>date:</strong><span>{{ formattedDate }}</span>
        </div>

          <pre>{{ JSON.stringify(submission, null, 2) }}</pre>
        </div>

      
        </div>
      </div>
    </dialog>
  </div>
</template>



<script>
export default {
  name: 'MovieDetailCard',
  props: {
    submission: {
      type: Object,
      required: true
    }
  },
  data(){
    return {
      dialogElement: null
    }
  },
  mounted() {
    this.dialog = this.$refs.dialog  // Get reference
  },
  methods: {
    showModal() {
      this.$refs.dialog?.showModal() 
    },
    closeDialog() {
            if (this.dialog) {
                this.dialog?.close();
            }
        },
      },
  computed: {
      movieTitle() {
        return this.submission?.movie.title || 'No name'
      },
      comment() {
        return this.submission?.comment || 'No description'
      },
      truncatedComment() {
        const desc = this.comment
        return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
      },
      author() {
        if (this.submission?.is_anonymous) {
          return 'Anonymus'
        }
        return this.submission?.author || 'Anonymus'
      },
      formattedDate() {
        if (!this.submission?.created_at) return ''
        return new Date(this.submission?.created_at).toLocaleDateString('ru-RU')
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