<template> 
   <div class="text">
        <h1 class="calendar-title">EVENT CALENDAR</h1>
   </div> 
   <div class="events-list"><Events></Events></div>
    <div class="events-list"><Events></Events></div>
</template>

<script>
import Events from '@/components/Events.vue'
export default {
  name: 'Calendar',
  components: {
    Events
  }}
</script>

<style>
.calendar-title {
  color: white;
  position: center;
}

.events-list {
  padding-top: 1rem;
  display: flex;
  flex-direction: row;
}



</style>