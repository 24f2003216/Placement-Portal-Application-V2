<script setup>
import { ref, onMounted } from 'vue'

const stats = ref(null)

onMounted(async () => {
  const res = await fetch('/admin/dashboard', { credentials: 'include' })
  if (res.ok) stats.value = await res.json()
})
</script>

<template>
<h2 class="mb-4">Admin Dashboard</h2>

<div v-if="stats">
  <div class="row text-center mb-4">
    <div class="col-md-3">
      <div class="card text-white bg-primary mb-3">
        <div class="card-body">
          <h5 class="card-title">Total Students</h5>
          <p class="card-text fs-3">{{ stats.total_students }}</p>
        </div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card text-white bg-success mb-3">
        <div class="card-body">
          <h5 class="card-title">Total Companies</h5>
          <p class="card-text fs-3">{{ stats.total_companies }}</p>
        </div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card text-white bg-warning mb-3">
        <div class="card-body">
          <h5 class="card-title">Total Drives</h5>
          <p class="card-text fs-3">{{ stats.total_drives }}</p>
        </div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card text-white bg-info mb-3">
        <div class="card-body">
          <h5 class="card-title">Total Applications</h5>
          <p class="card-text fs-3">{{ stats.total_applications }}</p>
        </div>
      </div>
    </div>
  </div>

  <div class="row">
    <div class="col-md-6 mb-3">
      <div class="card border-danger">
        <div class="card-body text-center">
          <h5>Pending Company Approvals</h5>
          <p class="fs-4">{{ stats.pending_companies }}</p>
          <router-link to="/admin/companies" class="btn btn-outline-danger btn-sm">Manage Companies</router-link>
        </div>
      </div>
    </div>
    <div class="col-md-6 mb-3">
      <div class="card border-danger">
        <div class="card-body text-center">
          <h5>Pending Drive Approvals</h5>
          <p class="fs-4">{{ stats.pending_drives }}</p>
          <router-link to="/admin/drives" class="btn btn-outline-danger btn-sm">Manage Drives</router-link>
        </div>
      </div>
    </div>
  </div>
</div>

<div v-else class="text-center mt-5">
  <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
</div>
</template>
