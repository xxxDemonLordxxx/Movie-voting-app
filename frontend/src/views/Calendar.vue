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
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
}

.calendar-title {
  color: white;
  position: center;
}

.events-list {
  padding-top: 2cap;
  display: flex;
  flex-direction: row;
}

</style>