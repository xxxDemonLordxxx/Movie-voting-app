<template>
    <div class="page-header">
      <router-link to="/polls" class="back-button">← BACK</router-link>
      <div class="title">
        <span class="poll-title">{{pollTitle}}</span> 
        <span class="page-title">POLL</span>
      </div>
      <p class="info-text">{{pollDescription}}: 
        {{ pollInfo?.winners }} movie{{ pollInfo?.winners > 1 ? 's' : '' }} to screen, 
        {{ submissionCount}} movie{{ submissionCount !== 1 ? 's' : '' }} to pick from
      </p>
    </div>
</template>

<script>
export default {
  name: 'MovieSubmissionCard',
  props: {
    pollInfo: {
      type: Object,
      required: true
    },
    submissions: {
      type: Array,
      required: true,
      default: () => []
    },
  },
  
  computed: {
    pollTitle() {
      return this.pollInfo?.title || 'No name'
    },
    pollDescription() {
      return this.pollInfo?.description || 'No description'
    },
    winners() {
      return this.pollInfo?.winners || 'No name'
    },
    submissionCount () {
      return this.submissions?.length || 0
    },
 }
}
</script>