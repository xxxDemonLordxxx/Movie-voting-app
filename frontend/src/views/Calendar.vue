<template> 
   <div class="text">
        <p class="text">OUR SEXY (VISUALLY) EVENT SCALENDAR (CONTENTS MAY VARY)</p>
   </div> 
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

.text{
color: white;
font-size: 16px;
position: center;
}

.events-list {
  padding-top: 2cap;
  display: flex;
  flex-direction: row;
}

p {
  word-break: break-all;
}
</style>