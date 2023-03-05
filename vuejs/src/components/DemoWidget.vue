<script setup>
import { ref } from 'vue'
import primevue from 'primevue'

// This is the good way to use a primevue component.
// If you try this :
// "import Button from 'primevue/button'"
// it'll work but not using externally provided primevue (via iife for instance) and lead to much bigger code
const Button = primevue.button

const Dialog = primevue.dialog

defineProps({
  msg: {
    type: String,
    required: true
  }
})
const displayModal = ref(false)

function openModal(ev) {
  displayModal.value = true
}
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a widget with
      <a href="https://vitejs.dev/" target="_blank" rel="noopener">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>.
    </h3>
    <Button v-bind:label="msg" icon="pi pi-check" iconPos="right" @click="openModal" />
    <Dialog
      header="Confirmation"
      v-model:visible="displayModal"
      :style="{ width: '350px' }"
      :modal="true"
      >{{ msg }}</Dialog
    >
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
}
/*
.p-button {
  margin-right: 0.5rem;
  text-align: center;
}

.p-buttonset .p-button {
  margin-right: 0;
}

.sizes .button {
  margin-bottom: 0.5rem;
  display: block;
}

.template .p-button i {
  line-height: 2.25rem;
}
*/
</style>
