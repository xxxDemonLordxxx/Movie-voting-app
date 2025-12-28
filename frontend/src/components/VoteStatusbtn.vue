<template>
<button class="btn admin" @click="changePollStatus" >{{ statusChange }} voting</button>
</template>

<script>
export default {
  name: 'VoteStatusbtn',
  props: {
    statusChange: String,
  },
  data() {
    return {
      showPopup: true,
      
    }
  },
    computed: {
    pollId() {
      const id = this.$route.params.id;
      console.log('Computed pollId from route:', id);
      return parseInt(id) || null;
    }
  },
methods: {
    async changePollStatus() {
      try {
        const response = await fetch(`http://localhost:8000/polls/${this.statusChange}/${this.pollId}`, {
        method: 'PATCH',  // Changed from POST to PATCH
        headers: {
          'Content-Type': 'application/json',
        },
        // Remove the body since poll_id is in the URL
      })
        if (response.ok) {
          alert('Poll status changed')
        } else {
          throw new Error('SENDING ERROR')
        }
      } catch (error) {
        console.error('Error:', error)
        alert('SENDING ERROR')
      } 
    },
}
}
</script>