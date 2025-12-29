<template>
        <div class="poll-box">
            <div class="unit-title">
                <p class="poll-title fringe">{{pollTitle}}</p> 
                <p class="poll-status">{{state_name}}</p>
            </div>
            <div class="unit-title date">
                <p class="text">{{pollStart}}</p> 
                <p class="text">---</p>
                <p class="text">{{pollEnd}}</p>
            </div>
          </div>
</template>

<script>
export default {
  name: 'PollUnit',
  props: {
    poll: {
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
    pollEnd() {
      return this.poll?.end|| 'no end date'
    },
    pollStart() {
      return this.poll?.start || 'no end date'
    }
  }
}
</script>

<style>
.fringe{
  color: rgba(149, 91, 153, 1);
  text-overflow: ellipsis;
  overflow: hidden;
  padding-right: 1rem;
}

.poll-status {
  color: rgb(0, 0, 0);
}
.unit-title {
  display: flex;
  flex-direction: row;
  justify-content: space-between;

}

.poll-box {
    display: flex;
    flex-direction: column;
    background-color: azure;
    padding: 1rem;
    padding-bottom: 0rem;
}




</style>

