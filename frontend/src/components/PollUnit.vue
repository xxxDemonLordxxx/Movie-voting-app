<template>
        <div class="poll-box">
            <div class="title">
                <p class="poll-title">{{pollTitle}}</p> 
                <p class="poll-status">{{state_name}}</p>
            </div>
            <div class="title date">
                <p class="text">13 JAN 2025</p> 
                <p class="text">---</p>
                <p class="text">13 JAN 2025</p>
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
  }
}
</script>

<style>
.poll-title {
  color: rgba(149, 91, 153, 1);
}

.poll-status {
  color: rgb(0, 0, 0);
}
.title {
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

.date {
  border-top: dotted 1px;
  border-color: gray;
    line-height: 1
}


</style>

