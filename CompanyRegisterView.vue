<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AlertMessage from '@/components/AlertMessage.vue'

const router = useRouter()
const form = ref({ name: '', hr_contact: '', website: '', username: '', password: '' })
const alert = ref({ message: '', category: '' })

async function handleRegister() {
  alert.value = { message: '', category: '' }
  const res = await fetch('/register/company', {
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
                <h3 class="card-title text-center mb-4">Company Registration</h3>

                <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

                <form @submit.prevent="handleRegister">
                    <div class="mb-3">
                        <label for="name" class="form-label">Company Name</label>
                        <input type="text" class="form-control" id="name" v-model="form.name" required>
                    </div>
                    <div class="mb-3">
                        <label for="hr_contact" class="form-label">HR Contact details</label>
                        <input type="text" class="form-control" id="hr_contact" v-model="form.hr_contact" required>
                    </div>
                    <div class="mb-3">
                        <label for="website" class="form-label">Company Website</label>
                        <input type="text" class="form-control" id="website" v-model="form.website"
                            placeholder="https://example.com" required>
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
                        <button type="submit" class="btn btn-warning">Register</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>
