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
      if (!this.poll?.end) return ''
        return new Date(this.poll?.created_at).toLocaleDateString('ru-RU')
    },
    pollStart() {
      if (!this.poll?.start) return ''
        return new Date(this.poll?.start).toLocaleDateString('ru-RU')
    },
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

