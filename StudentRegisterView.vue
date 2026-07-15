<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AlertMessage from '@/components/AlertMessage.vue'

const router = useRouter()
const form = ref({ name: '', contact: '', username: '', password: '' })
const alert = ref({ message: '', category: '' })

async function handleRegister() {
  alert.value = { message: '', category: '' }
  const res = await fetch('/register/student', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  const data = await res.json()
  if (res.ok) {
    alert.value = { message: data.message, category: 'success' }
    setTimeout(() => router.push('/login'), 1500)
  } else {
    alert.value = { message: data.error, category: 'danger' }
  }
}
</script>

<template>
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow-sm mt-5">
            <div class="card-body">
                <h3 class="card-title text-center mb-4">Student Registration</h3>

                <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

                <form @submit.prevent="handleRegister">
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" v-model="form.name" required>
                    </div>
                    <div class="mb-3">
                        <label for="contact" class="form-label">Contact / Email</label>
                        <input type="text" class="form-control" id="contact" v-model="form.contact" required>
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" v-model="form.username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" v-model="form.password" required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-success">Register</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>
