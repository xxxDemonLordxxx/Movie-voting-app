<template>
    <div class="page-header">
      <div class="navigator">
        <router-link to="/polls" class="back-button">← BACK</router-link>
         <div class="title">
            <span class="poll-title">{{pollTitle}}</span> 
            <span class="page-title">poll</span>
          </div>
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

<style>
  .text{
color: white;
font-size: 16px;
position: center;
}

.info-text {
  overflow: visible;
  word-wrap: break-word;
}
.back-button {
  padding-bottom: 30px;
  color:#0f6f62;
}

.navigator {
  display: inline-flex; 
  justify-content: space-between; 
  width: 100%; 
  align-self: center;
  padding-bottom: 1rem;
}

.page-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-top: 1rem;

}
.poll-title {
  color: rgba(149, 91, 153, 1);
  text-align: center;
  text-transform: uppercase;
}

.page-title {
  color: aliceblue;
  padding-bottom: 1cap;
    text-transform: uppercase;
}

span {
  display: inline-block;
  padding: 5px;
}
</style>
