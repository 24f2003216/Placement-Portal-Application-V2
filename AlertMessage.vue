<script setup>
defineProps({
  message: { type: String, default: '' },
  category: { type: String, default: 'info' }  // Bootstrap: success, danger, warning, info
})
const emit = defineEmits(['dismiss'])
</script>

<template>
  <div v-if="message" class="alert" :class="`alert-${category} alert-dismissible fade show`" role="alert">
    {{ message }}
    <button type="button" class="btn-close" @click="emit('dismiss')" aria-label="Close"></button>
  </div>
</template>
