<template>
  <div class="movie-detail-card">
    <div class="card-header">
      <h1 class="movie-title">{{ movieTitle }}</h1>
    </div>
    
    <div class="card-body">
      <div class="description-section">
        <h3>pitch</h3>
        <p class="movie-description">{{ comment }}</p>
      </div>
      
        <div class="submission-meta">
        <div class="meta-item">
          <strong>offered by:</strong>
          <span>{{ author }}</span>
        </div>
        
        <div class="meta-item">
          <strong>date:</strong>
          <span>{{ formattedDate }}</span>
        </div>

        <div>
          <img 
          v-if="imageUrl && imageUrl.trim()" 
          :src="imageUrl"/>
        </div>

              <div style=" padding: 10px; margin: 10px 0;">
            <strong>Debug image_url:</strong> "{{ imageUrl }}"
            <br>
            <strong>Type:</strong> {{ typeof imageUrl }}
            <br>
            <strong>Length:</strong> {{ imageUrl?.length || 0 }}
          </div>
          
          <!-- Conditional image -->
          <img 
            v-if="isRealImageUrl"
            :src="imageUrl" 
            :alt="submission.title"
            @error="console.error('Image failed to load:', imageUrl)"
          />
          <div v-else></div>

          <pre>{{ JSON.stringify(submission, null, 2) }}</pre>
          <p><strong>submission.image_url:</strong> "{{ submission.image_url }}"</p>
           <p><strong>Truthy?</strong> {{ !!submission.image_url }}</p>
        </div>

      
      </div>
    </div> 
      <CopyButton />
</template>



<script>
import CopyButton from './CopyButton.vue'
export default {
  components: { CopyButton },
  name: 'MovieDetailCard',
  props: {
    submission: {
      type: Object,
      required: true
    }
  },
  computed: {
    movieTitle() {
      return this.submission?.movie?.title || 'No name'
    },
    comment() {
      return this.submission.comment || 'No description'
    },
    imageUrl() {
      return this.submission.image_url
    },
    isRealImageUrl() {
      // Only show if it ends with image file extension
      if (!this.imageUrl) return false;
      
      const imgExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
      const url = this.imageUrl.toLowerCase();
      
      return imgExtensions.some(ext => url.endsWith(ext));
    },
    truncatedComment() {
      const desc = this.comment
      return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
    },
    author() {
      if (this.submission.is_anonymous) {
        return 'Anonymus'
      }
      return this.submission.author || 'Anonymus'
    },
    formattedDate() {
      if (!this.submission.created_at) return ''
      return new Date(this.submission.created_at).toLocaleDateString('ru-RU')
    }
  }
}
</script>

<style scoped>
.hidden-content {
  display: none;
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
  padding-top: 1.5rem;
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
  
  .submission-meta {
    padding-top: 1.25rem;
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