<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AlertMessage from '@/components/AlertMessage.vue'

const route = useRoute()
const driveId = route.params.id
const driveData = ref(null)
const alert = ref({ message: '', category: '' })

async function loadApplicants() {
  const res = await fetch(`/company/applicants/${driveId}`, { credentials: 'include' })
  if (res.ok) driveData.value = await res.json()
}

async function updateStatus(appId, status) {
  const res = await fetch(`/company/applicants/update/${appId}/${status}`, { credentials: 'include' })
  const data = await res.json()
  alert.value = { message: data.message || data.error, category: res.ok ? 'success' : 'danger' }
  loadApplicants()
}

onMounted(loadApplicants)
</script>

<template>
<div v-if="driveData">
  <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

  <div class="mb-4">
      <h2>Applicants for: {{ driveData.job_title }}</h2>
      <router-link to="/company/dashboard" class="btn btn-sm btn-outline-secondary">&larr; Back to Dashboard</router-link>
  </div>

  <table class="table table-striped table-hover">
      <thead class="table-dark">
          <tr>
              <th>Name</th>
              <th>Contact</th>
              <th>Date Applied</th>
              <th>Resume</th>
              <th>Status</th>
              <th>Action</th>
          </tr>
      </thead>
      <tbody>
          <tr v-for="app in driveData.applications" :key="app.id">
              <td>{{ app.student_name }}</td>
              <td>{{ app.student_contact }}</td>
              <td>{{ app.date_applied }}</td>
              <td>
                  <a v-if="app.resume_filename" :href="`/static/uploads/${app.resume_filename}`"
                      target="_blank" class="btn btn-sm btn-info">View Resume</a>
                  <span v-else>Not Provided</span>
              </td>
              <td>
                  <span v-if="app.status === 'Applied'" class="badge bg-secondary">Applied</span>
                  <span v-else-if="app.status === 'Shortlisted'" class="badge bg-primary">Shortlisted</span>
                  <span v-else-if="app.status === 'Selected'" class="badge bg-success">Selected</span>
                  <span v-else-if="app.status === 'Rejected'" class="badge bg-danger">Rejected</span>
              </td>
              <td>
                  <div class="dropdown">
                      <button class="btn btn-sm btn-outline-dark dropdown-toggle" type="button"
                          data-bs-toggle="dropdown" aria-expanded="false">
                          Update Status
                      </button>
                      <ul class="dropdown-menu">
                          <li><a class="dropdown-item" href="#" @click.prevent="updateStatus(app.id, 'Shortlisted')">Shortlist</a></li>
                          <li><a class="dropdown-item" href="#" @click.prevent="updateStatus(app.id, 'Selected')">Select</a></li>
                          <li><a class="dropdown-item" href="#" @click.prevent="updateStatus(app.id, 'Rejected')">Reject</a></li>
                      </ul>
                  </div>
              </td>
          </tr>
          <tr v-if="driveData.applications.length === 0">
              <td colspan="6" class="text-center">No applications yet.</td>
          </tr>
      </tbody>
  </table>
</div>

<div v-else class="text-center mt-5">
  <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
</div>
</template>
