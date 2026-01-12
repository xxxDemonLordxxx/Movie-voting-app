<template>
  <div class="voting-form-container">
    <!-- Dynamic inputs based on winner count -->
    <div v-for="(position, index) in winnerPositions" :key="index" class="input-group">
      <div class="position-label">
        <span class="number">{{ getPositionLabel(index) }}</span>
      </div>
      <p class="search-pretty">(</p>
      <div class="form-textarea iconed-selector" @click="openPopup(index)">
        <input
          type="text"
          :value="getDisplayValue(index)"
          :placeholder="`Select ${getPositionLabel(index)} choice...`"
          readonly
          class="form-textarea voting-area"
          :class="{ 'has-selection': selectedSubmissions[index] }"
        />
        <span class="selector-icon">▼</span>
      </div>
      <p class="search-pretty">)</p>
      <!-- Clear button for filled positions -->
      <button 
        v-if="selectedSubmissions[index]" 
        @click="clearPosition(index)"
        class="clear-position-btn"
      >
        ×
      </button>
    </div>

    <div v-show="isOpen" class="popup-overlay" @click.self="closePopup">
      <div class="popup-container" @click.stop>
        <div class="popup-tools">
          <div class="popup-header">
            <button @click="closePopup" class="close-btn">×</button>    
            <div class="header-actions">
              <button 
                @click="confirmSelection" 
                :disabled="!tempSelectedSubmission"
                class="btn primary"
              >
                Select {{ getPositionLabel(currentPositionIndex) }}
              </button>
            </div>
          </div>

        <!-- Search Filter -->
          <div class="popup-search">
            <p class="search-pretty search-pretty-form">(</p>
            <input
              type="text"
              v-model="searchQuery"
              :placeholder="`Search from a selection of ${submissionCount} film${submissionCount !== 1 ? 's' : '' }...`"
              class="form-textarea popup-input"
              ref="searchInput"
            >
            <p class="search-pretty search-pretty-form">)</p>
          </div>
      </div>
        

        <div class="card-body">
          <MovieSubmissionCard
          v-for="submission in filteredSubmissions"
          :key="submission.id"
          :submission="submission" 
          @click="setTempSelection(submission)"
          :temp-selected="isTempSelected(submission)"
          :unavailable="isAlreadySelected(submission)"
          @show-dialog="$emit('show-dialog', $event)"
          class="Card"
          />
        </div>

        <!-- Submissions List as Cards -->
        <!-- Submissions List as Cards -->
        <!-- <div class="popup-content-cards">
            <div
            v-for="submission in filteredSubmissions"
            :key="submission.id"
            > 
            <div  @click="setTempSelection(submission)"
                  :class="['movie-suggestion-card', { 
                'temp-selected': isTempSelected(submission),
                'unavailable': isAlreadySelected(submission) 
                }]">
              <div class="card-content">
                <div class="card-header">
                  <h3 class="movie-title">{{ getSubmissionTitle(submission) }}</h3>
                  <div v-if="isAlreadySelected(submission)" class="unavailable-badge">
                    {{ getPositionOfSubmission(submission) + 1 }}
                  </div>
                </div>
                
                <p class="movie-description">
                  {{ truncateComment(submission.comment) }}
                </p>
                
                <div class="submission-info">
                  <span class="suggester">
                    {{ getSubmissionAuthor(submission) }}
                  </span>
                  <span class="date">{{ formatDate(submission.created_at) }}</span>
                </div>
              </div>
            <div class="btn-block">
            <img src='@/assets/more_button.png' @click="viewSubmission(submission.id)" class="more-button" />
            </div>
      </div> -->
          
          <div v-if="availableSubmissions.length === 0" class="no-results">
            No films left
          </div>
        </div>
      </div>
      <!-- </div> -->
    <!-- </div> -->
  </div>
</template>

<script>
import MovieDetailCard from './MovieDetailCard.vue';
import MovieSubmissionCard from './MovieSubmissionCard.vue';

export default {
  name: 'VotingInput',
  components: {
    MovieSubmissionCard,
    MovieDetailCard
  },
  props: {
    // Array of submission objects
    submissions: {
      type: Array,
      required: true,
      default: () => []
    },
    
    // Poll info object containing winners
    pollInfo: {
      type: Object,
      default: null
    },
    
    // Initial value (comma-separated string of IDs)
    value: {
      type: String,
      default: ''
    },
    
    // Maximum selections (falls back to winners from pollInfo)
    maxSelections: {
      type: Number,
      default: null
    }
  },
  
    data() {
    return {
        isOpen: false,
        searchQuery: '',
        currentPositionIndex: 0,
        selectedSubmissions: [], // Array where index = position
        tempSelectedSubmission: null // Temporary selection before confirming
        };
    },
  
  computed: {
    // Number of winner positions based on pollInfo or prop
    winnerCount() {
      if (this.maxSelections) return this.maxSelections;
      if (this.pollInfo?.winners) return this.pollInfo.winners;
      return 1; // Default to 1 if not specified
    },
    
    // Array of winner positions [0, 1, 2, ...]
    winnerPositions() {
      return Array.from({ length: this.winnerCount }, (_, i) => i);
    },
    
    // Filter submissions based on search
    filteredSubmissions() {
      if (!this.searchQuery.trim()) return this.submissions;
      
      const query = this.searchQuery.toLowerCase();
      return this.submissions.filter(submission => {
        const title = this.movieTitle(submission).toLowerCase();
        const comment = submission.comment?.toLowerCase() || '';
        
        return title.includes(query) || comment.includes(query);
      });
    },
    
    // Submissions available for current position (not already selected in other positions)
    availableSubmissions() {
      return this.filteredSubmissions.filter(submission => 
        !this.isAlreadySelected(submission)
      );
    },
    
    // Check if there are selections in other positions
    hasSelectionsInOtherPositions() {
      return this.selectedSubmissions.some((sub, index) => 
        sub && index !== this.currentPositionIndex
      );
    },
    
    // Formatted output string (comma-separated IDs)
    outputString() {
      return this.selectedSubmissions
        .map(sub => sub?.id || '')
        .filter(id => id !== '')
        .join(',');
    },
    submissionCount () {
      return this.submissions?.length || 0
    },
  },
  
  watch: {
    // Sync with external v-model
    value: {
      immediate: true,
      handler(newVal) {
        this.parseInitialValue(newVal);
      }
    },
    
    // Update external v-model when selections change
    outputString(newVal) {
      this.$emit('input', newVal);
    },
    
    // Reset current position when popup closes
    isOpen(newVal) {
      if (!newVal) {
        this.currentPositionIndex = 0;
        this.searchQuery = '';
      }
    }
  },
  
  mounted() {
    // Initialize selected submissions array
    this.isOpen = false;
    this.selectedSubmissions = Array(this.winnerCount).fill(null);
    this.parseInitialValue(this.value);
  },
  
    methods: {
    // Parse initial comma-separated string
    parseInitialValue(valueString) {
        if (!valueString) return;
        
        const ids = valueString.split(',').map(id => id.trim()).filter(id => id);
        
        ids.forEach((id, index) => {
        if (index < this.winnerCount) {
            const submission = this.submissions.find(sub => sub.id.toString() === id.toString());
            if (submission) {
            this.selectedSubmissions[index] = submission;
            }
        }
        });
    },
    
    // Get position label (1st, 2nd, 3rd, etc.)
    getPositionLabel(index) {
        const suffixes = ['th', 'st', 'nd', 'rd'];
        const v = index + 1;
        const suffix = suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0];
        return `${v}${suffix}`;
    },
    
    // Get display value for a specific position
    getDisplayValue(index) {
        const submission = this.selectedSubmissions[index];
        return submission ? this.movieTitle(submission) : '';
    },
    
    // Open popup for specific position
    openPopup(positionIndex) {
        this.currentPositionIndex = positionIndex;
        this.isOpen = true;
        this.searchQuery = '';
        this.tempSelectedSubmission = null; // Reset temp selection
        
        // Focus search input after popup opens
        this.$nextTick(() => {
        if (this.$refs.searchInput) {
            this.$refs.searchInput.focus();
        }
        });
    },
    
    closePopup() {
        this.isOpen = false;
        this.searchQuery = '';
        this.tempSelectedSubmission = null;
    },
    
    // Set temporary selection when clicking a card
    setTempSelection(submission) {
        if (this.isAlreadySelected(submission)) {
        return; // Don't allow selecting same movie in multiple positions
        }
        this.tempSelectedSubmission = submission;
    },
    
    // Check if submission is currently temporarily selected
    isTempSelected(submission) {
        return this.tempSelectedSubmission && 
            this.tempSelectedSubmission.id === submission.id;
    },
    
    // Confirm the temporary selection
    confirmSelection() {
        if (!this.tempSelectedSubmission) return;
        
        this.selectedSubmissions[this.currentPositionIndex] = this.tempSelectedSubmission;
        this.closePopup();
    },
    
    // Clear a specific position
    clearPosition(index) {
        this.selectedSubmissions[index] = null;
    },
    
    // Check if submission is already selected in any position
    isAlreadySelected(submission) {
        return this.selectedSubmissions.some(sub => 
        sub && sub.id === submission.id
        );
    },
    
    // Get position index of a selected submission
    getPositionOfSubmission(submission) {
        return this.selectedSubmissions.findIndex(sub => 
        sub && sub.id === submission.id
        );
    },
    
    // Helper methods for submission data
    movieTitle(submission) {
        return submission?.movie?.title || submission?.title || 'Unknown Movie';
    },

    truncatedComment(comment) {
        if (!comment) return 'No description provided';
        const maxLength = 120;
        return comment.length > maxLength 
        ? comment.substring(0, maxLength) + '...' 
        : comment;
    },

    author(submission) {
        return submission?.author || 'Anonymous';
    },

    formattedDate() {
      if (submission?.created_at) return ''
      return new Date(submission?.created_at).toLocaleDateString('en-EN')
    },
    },
};
</script>

<style scoped>
.voting-form-container {
  width: 100%;
}



.winner-input-group {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  padding: 10px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
}

.position-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.position-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #4a90e2;
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.position-text {
  font-weight: 500;
  color: #495057;
}

.selector-input {
  flex: 1;
  position: relative;
  cursor: pointer;
}

.selector-input-field {
  width: 100%;
  padding: 12px 40px 12px 15px;
  font-size: 15px;
  border: 2px solid #dee2e6;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.2s;
  box-sizing: border-box;
}



.selector-input-field.has-selection {
  color: rgb(82, 39, 85);
}

.selector-input-field:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.selector-icon {
  color: #257e79;
  font-size: 12px;
}

.iconed-selector {
  display: flex;
  
}

.clear-position-btn {
  padding: 8px 12px;
  background: #e74c3c;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  transition: background-color 0.2s;
}

.clear-position-btn:hover {
  background: #c0392b;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-container {
  background: rgb(24, 23, 25);
  width: 90%;
  max-width: 95vw;
  max-height: 85vh; /* Slightly smaller to ensure fit */
  overflow-y: scroll;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: popup-fade-in 0.2s ease-out; /* Add animation */
}

.popup-tools {
  background: rgb(24, 23, 25);
  position: fixed;
  width: 89vw;
  z-index: 1000;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.611);
}


  .movie-suggestion-card {
    margin-left: -49vw;
    position: relative;
    left: 50%;
    max-width: 95vw;
}

.card-body{
  margin-top: 8rem;
}

.card {
  margin: 1rem
}
@keyframes popup-fade-in {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}



.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.popup-header h3 {
  margin: 0;
  font-size: 20px;
  color: #ffffff;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-block{
  display: flex;
  flex-direction: row;
  color: white;
  border-color: gray;
  border-width: 0.1rem;
  border-style: dotted;
  flex-shrink:2;
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

.close-btn:hover {
  color: #333;
}

.selection-summary {
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.summary-title {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 8px;
}

.selected-positions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-position-tag {
  background: #e9ecef;
  padding: 6px 12px;
  font-size: 13px;
  color: #495057;
  border: 1px solid #dee2e6;
}

.selected-badge {
  color:#333;
}

.popup-search {
  padding: 0rem;
  display: flex;
  background-color: white;
  margin: 0 1rem 0rem 1rem;
  line-height: 1.2;
}

.search-input {
  width: 100%;
  border: 2px solid #dee2e6;
  font-size: 0.6rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
  margin: 0.2rem 0 0.3rem 0;
}
.voting-area {
  text-decoration: rgba(149, 91, 153, 1) wavy underline 0.1rem;
}

.form-input,
.form-textarea {
  width: 100%;
  border: 0;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.popup-input {
  color: rgba(149, 91, 153, 1);
}
.has-selection{
  text-decoration: none;
  color: rgb(82, 39, 85);
}



.d
.search-input:focus {
  outline: none;
  border-color: #dee2e6;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.popup-content-cards {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.submission-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.2s;
  gap: 16px;

}

.submission-card:hover:not(.unavailable) {
  background-color: #48655a;
}

.submission-card.unavailable {
  opacity: 0.6;
  cursor: not-allowed;
  border: dotted rgb(228, 204, 131) 3px
}


.card-content {
  width: 80vw;
  flex-grow: 3;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  max-width: 80vw;
}

.movie-title {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  max-width: 3rem;
}

.unavailable-badge {
  background: #6c757d;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  
}

.movie-description {
  margin: 0 0 12px 0;
  color: #ffffff;
  font-size: 0.8rem;
  line-height: 1.5;
}

.submission-info {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #ffffff;
}

.suggester {
  font-weight: 500;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.select-btn, .view-details-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.select-btn {
  background: #4a90e2;
  color: white;
}

.select-btn:hover {
  background: #3a7bc8;
}

.view-details-btn {
  background: #e9ecef;
  color: #495057;
}

.view-details-btn:hover {
  background: #dee2e6;
}

.no-results {
  padding: 40px 20px;
  text-align: center;
  color: #6c757d;
}

.search-pretty-form{
  align-self: flex-end
}
</style>