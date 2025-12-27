<template> 
   <div class="text">
        <h1 class="calendar-title">EVENT CALENDAR</h1>
   </div> 
   <div class="events-list">
    <EventUnit
      v-for="(event,index) in events" 
            :key="event.id || index "
            :event="event"
    />
    </div>
</template>

<script>
import EventUnit from '@/components/EventUnit.vue'
export default {
  name: 'Calendar',
  components: {
    EventUnit
  },
  
  data() {
    return {
      events: [],
      loading: false,
      error: null,
    }
  },
  async mounted() {
    await this.fetchEvents()

  },
  methods: {
    async fetchEvents() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch(`http://localhost:8000/events/`)
        if (response.ok) {
          this.events = await response.json()  // Get the full response
            console.log('Loaded event info:', this.events)
          } else {
            throw new Error(`HTTP error! status: ${response.status}`)
          }
        } catch (error) {
          console.error('Error loading events:', error)
          this.error = 'Mistake when loading the events: ' + error.message
        } finally {
          this.loading = false
        }
      },
    viewEvent(id) {
      this.$router.push(`/events/${id}`)
    }
  }
}
</script>

<style>
.calendar-title {
  color: white;
  text-align: center;
}

.events-list {
  padding-top: 1rem;
  display: flex;
  flex-direction: row;
}



</style>