<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import auth from '@/store/authentication.js'
import AlertMessage from '@/components/AlertMessage.vue'

const router = useRouter()
const username = ref('')
const password = ref('')
const alert = ref({ message: '', category: '' })

async function handleLogin() {
  alert.value = { message: '', category: '' }
  const { ok, data } = await auth.login(username.value, password.value)
  if (ok) {
    if (data.role === 'admin') router.push('/admin/dashboard')
    else if (data.role === 'company') router.push('/company/dashboard')
    else if (data.role === 'student') router.push('/student/dashboard')
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
                <h3 class="card-title text-center mb-4">Login to Placement Portal</h3>

                <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" v-model="username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" v-model="password" required>
                    </div>
                    <div class="d-grid mb-3">
                        <button type="submit" class="btn btn-primary">Login</button>
                    </div>
                </form>

                <div class="text-center mt-3">
                    <p>Don't have an account?</p>
                    <router-link to="/register/student" class="btn btn-outline-secondary btn-sm">Register as Student</router-link>
                    <router-link to="/register/company" class="btn btn-outline-secondary btn-sm ms-1">Register as Company</router-link>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
