vue

<template>
  <div v-if="showPopup" class="popup-overlay">
    <div class="popup-content">
      <p class="info-text">
        {{ psa }}
        <button @click="closePopup" class="close-link">{{haha}}</button> 
        {{ psa2}}
      </p>
    </div>
  </div>
</template>


<script>
export default {
  name: 'PopupWindow',
  props: {
    psa: String,
    haha: String,
    psa2: String
  },
  data() {
    return {
      showPopup: true,
      
    }
  },
  methods: {
    closePopup() {
      this.showPopup = false
    }
  },
}
</script>

<style scoped>
.popup-overlay {
position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: rgb(24, 23, 25);
  padding: 4rem 0rem 10rem 0rem;
  max-width: 80%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.close-link {
  background: none;
  border: none;
  color: rgba(149, 91, 153, 1);
  cursor: pointer;
  padding: 0;
  font-size: inherit;
  font-family: inherit;
}

.close-link:hover {
  color: rgba(149, 91, 153, 1);
  text-decoration: none;
}
</style>