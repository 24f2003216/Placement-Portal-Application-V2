<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AlertMessage from '@/components/AlertMessage.vue'

const router = useRouter()
const data = ref(null)
const alert = ref({ message: '', category: '' })

async function loadDashboard() {
  const res = await fetch('/company/dashboard', { credentials: 'include' })
  if (res.ok) data.value = await res.json()
}

async function doAction(url, confirmMsg) {
  if (confirmMsg && !confirm(confirmMsg)) return
  const res = await fetch(url, { credentials: 'include' })
  const json = await res.json()
  alert.value = { message: json.message || json.error, category: res.ok ? 'success' : 'danger' }
  loadDashboard()
}

onMounted(loadDashboard)
</script>

<template>
<div v-if="data">
  <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

  <div class="row mb-4">
      <div class="col-md-8">
          <h2>Company Dashboard: {{ data.company.name }}</h2>
          <p><strong>HR Contact:</strong> {{ data.company.hr_contact }} | <strong>Website:</strong>
              <a :href="data.company.website" target="_blank">{{ data.company.website }}</a></p>
      </div>
      <div class="col-md-4 text-end mt-2">
          <router-link to="/company/drives/create" class="btn btn-primary">Create New Drive</router-link>
      </div>
  </div>

  <div class="row">
      <div class="col-md-6 mb-3">
          <div class="card bg-light">
              <div class="card-body text-center">
                  <h5>Total Drives Posted</h5>
                  <p class="fs-4">{{ data.drives.length }}</p>
              </div>
          </div>
      </div>
      <div class="col-md-6 mb-3">
          <div class="card bg-light">
              <div class="card-body text-center">
                  <h5>Total Applications Received</h5>
                  <p class="fs-4">{{ data.apps_count }}</p>
              </div>
          </div>
      </div>
  </div>

  <h3 class="mt-4 mb-3">Your Placement Drives</h3>
  <table class="table table-striped table-hover">
      <thead class="table-dark">
          <tr>
              <th>Job Title</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Applicants</th>
              <th>Actions</th>
          </tr>
      </thead>
      <tbody>
          <tr v-for="drive in data.drives" :key="drive.id">
              <td>{{ drive.job_title }}</td>
              <td>{{ drive.deadline }}</td>
              <td>
                  <span v-if="drive.status === 'Pending'" class="badge bg-warning text-dark">Pending Admin Approval</span>
                  <span v-else-if="drive.status === 'Approved'" class="badge bg-success">Active/Approved</span>
                  <span v-else-if="drive.status === 'Closed'" class="badge bg-secondary">Closed</span>
              </td>
              <td>{{ drive.applicants_count }}</td>
              <td>
                  <router-link :to="`/company/applicants/${drive.id}`" class="btn btn-sm btn-info me-1">View Applicants</router-link>
                  <template v-if="drive.status !== 'Closed'">
                      <router-link :to="`/company/drives/edit/${drive.id}`" class="btn btn-sm btn-secondary me-1">Edit</router-link>
                      <button class="btn btn-sm btn-warning me-1"
                          @click="doAction(`/company/drives/close/${drive.id}`, 'Close this drive?')">Close</button>
                  </template>
                  <button class="btn btn-sm btn-danger"
                      @click="doAction(`/company/drives/delete/${drive.id}`, 'Are you sure you want to delete this drive? All related applications will be deleted.')">Delete</button>
              </td>
          </tr>
          <tr v-if="data.drives.length === 0">
              <td colspan="5" class="text-center">No placement drives created yet.</td>
          </tr>
      </tbody>
  </table>
</div>

<div v-else class="text-center mt-5">
  <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
</div>
</template>
