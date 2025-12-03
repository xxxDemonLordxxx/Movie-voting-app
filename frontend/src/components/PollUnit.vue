<template>
        <router-link to="/voting" class="poll-box">
            <div class="title">
                <span class="poll-title">{{pollTitle}}</span> 
                <span class="poll-status">{{state_name}}</span>
            </div>
            <p class="text">DATE - DATE</p>
        </router-link>
</template>

<script>
export default {
  name: 'PollsUnit',
  props: {
    polls: {
      type: Object,
      required: true
    }
  },
  computed: {
    pollTitle() {
      return this.poll?.title || 'No name'
    },
    state_name() {
      return this.poll?.state_name || 'No description'
    },
}
}
</script>

<style>
.poll-title {
  color: rgba(149, 91, 153, 1);
}

.poll-status {
  color: rgb(0, 0, 0);
  padding-bottom: 1cap;
}
.title {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.layout {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
}

span {
  display: inline-block;
  padding: 5px;
}

.poll-box {
    display: flex;
    flex-direction: column;
    background-color: azure;
    padding: 1rem;
}

.header-text {
    color:rgba(244, 233, 172, 1) ;
    inset-inline: auto;
    font-size: 23px
}

.header-text2 {
    color:rgba(149, 91, 153, 1);
    inset-inline: auto;
    font-size: 24px
}

.info-text {
    color:rgba(244, 233, 172, 1) ;
    text-align: center;
    
}

.page-signal{
  margin: auto;
}
</style>

