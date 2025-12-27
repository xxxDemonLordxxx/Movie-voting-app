<template>
    <div class="page-header">
      <router-link to="/polls" class="back-button">← BACK</router-link>
      <div class="title">
        <span class="poll-title">{{pollTitle}}</span> 
        <span class="page-title">POLL</span>
      </div>
      <p class="info-text">{{pollDescription}}</p>
    </div>
</template>

<script>
export default {
  name: 'MovieSubmissionCard',
  props: {
    pollInfo: {
      type: Object,
      required: true
    }
  },
  computed: {
    pollTitle() {
      return this.pollInfo?.title || 'No name'
    },
    pollDescription() {
      return this.pollInfo?.description || 'No description'
    },
    }
}
</script>