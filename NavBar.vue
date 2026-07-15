<script setup>
import { useRouter } from 'vue-router'
import auth from '@/store/authentication.js'

const router = useRouter()

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
    <div class="container">
      <a class="navbar-brand" href="#">Placement Portal</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
        data-bs-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault"
        aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav ms-auto mb-2 mb-md-0">

          <!-- Admin links -->
          <template v-if="auth.state.user && auth.state.user.role === 'admin'">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/companies">Companies</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/students">Students</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/drives">Drives</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/applications">Applications</router-link>
            </li>
          </template>

          <!-- Company links -->
          <template v-else-if="auth.state.user && auth.state.user.role === 'company'">
            <li class="nav-item">
              <router-link class="nav-link" to="/company/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/company/drives/create">Post a Drive</router-link>
            </li>
          </template>

          <!-- Student links -->
          <template v-else-if="auth.state.user && auth.state.user.role === 'student'">
            <li class="nav-item">
              <router-link class="nav-link" to="/student/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/student/history">History</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/student/profile">Profile</router-link>
            </li>
          </template>

          <!-- Logged in: Logout -->
          <li class="nav-item" v-if="auth.state.user">
            <a class="nav-link text-danger" href="#" @click.prevent="handleLogout">
              Logout ({{ auth.state.user.username }})
            </a>
          </li>

          <!-- Guest links -->
          <template v-if="!auth.state.user">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register/student">Student Register</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register/company">Company Register</router-link>
            </li>
          </template>

        </ul>
      </div>
    </div>
  </nav>
</template>
