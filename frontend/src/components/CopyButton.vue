<template>
  <div v-if="isSupported">
    <button class="btn btn-primary">
      <!-- by default, `copied` will be reset in 1.5s -->
      <span v-if="!copied">Copy</span>
      <span v-else>Copied!</span>
    </button>
  </div>
  <p v-else>
    Your browser does not support Clipboard API
  </p>
</template>


<script setup lang="ts">

</script>


<style>
.btn {
  padding: 4px 12px;
  border: none;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #065f53;
  color: white;
  padding: 4px 12px
}
.btn-primary:hover:not(:disabled) {
  background-color: #0f6f62;
}
</style>