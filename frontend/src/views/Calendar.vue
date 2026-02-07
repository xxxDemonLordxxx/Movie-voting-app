<template> 
   <div class="text">
        <h1 class="calendar-title">EVENT CALENDAR</h1>
   </div> 
   <div v-if="isAdmin" class="NewEventButton">
        <NewEventButton />
    </div>
   <div class="events-list">
    <EventUnit
      v-for="event in events" 
      :key="event.id"
      :event="event"
      @open-event="showEvent(event.id)"
    />
    </div>

</template>

<script>
import EventUnit from '@/components/EventUnit.vue'
import NewEventButton from '@/components/NewEventButton.vue'
export default {
  name: 'Calendar',
  components: {
    EventUnit,
    NewEventButton,

  },
  
  data() {
    return {
      events: [],
      loading: false,
      error: null,
      isAdmin: false,
      event:null
    }
  },
  async mounted() {
    await this.fetchEvents(), this.checkAdmin();

  },
  methods: {
    async fetchEvents() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch(`http://observational.website/events/`)
        if (response.ok) {
          this.events = await response.json()  // Get the full response
            console.log('Loaded event info')
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
      checkAdmin() {
      const storedAdmin = localStorage.getItem('isAdmin')
      this.isAdmin = storedAdmin === 'true'
    },
    showEvent(id) {
      this.$router.push(`/event/${id}`)
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
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100vw;
  position: absolute;
  left: 0;
}



</style>