<script setup>
import { ref, onMounted } from 'vue'
import AlertMessage from '@/components/AlertMessage.vue'

const data = ref(null)
const alert = ref({ message: '', category: '' })
const selectedDrive = ref(null)

async function loadDashboard() {
  const res = await fetch('/student/dashboard', { credentials: 'include' })
  if (res.ok) data.value = await res.json()
}

async function applyDrive(driveId, jobTitle, companyName) {
  if (!confirm(`Confirm your application for ${jobTitle} at ${companyName}?`)) return
  const res = await fetch(`/student/apply/${driveId}`, { credentials: 'include' })
  const json = await res.json()
  alert.value = { message: json.message || json.error, category: res.ok ? 'success' : 'danger' }
  if (res.ok) loadDashboard()
}

function openModal(drive) {
  selectedDrive.value = drive
}

function closeModal() {
  selectedDrive.value = null
}

onMounted(loadDashboard)
</script>

<template>
<div v-if="data">
  <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

  <div class="row mb-4">
      <div class="col-md-8">
          <h2>Student Dashboard: {{ data.student.name }}</h2>
      </div>
      <div class="col-md-4 text-end mt-2">
          <router-link to="/student/profile" class="btn btn-outline-primary">Update Profile</router-link>
      </div>
  </div>

  <div class="row">
      <div class="col-md-6 mb-3">
          <div class="card bg-light">
              <div class="card-body text-center">
                  <h5>Applications Submitted</h5>
                  <p class="fs-4">{{ data.applications.length }}</p>
              </div>
          </div>
      </div>
      <div class="col-md-6 mb-3">
          <div class="card bg-light">
              <div class="card-body text-center">
                  <h5>Shortlisted/Selected</h5>
                  <p class="fs-4">{{ data.shortlisted_count }}</p>
              </div>
          </div>
      </div>
  </div>

  <h3 class="mt-4 mb-3">Available Placement Drives</h3>
  <div class="row">
      <div v-for="drive in data.available_drives" :key="drive.id" class="col-md-4 mb-3">
          <div class="card shadow-sm h-100">
              <div class="card-body d-flex flex-column">
                  <h5 class="card-title">{{ drive.job_title }}</h5>
                  <h6 class="card-subtitle mb-2 text-muted">{{ drive.company_name }}</h6>
                  <p class="card-text">
                      <strong>Eligibility:</strong> {{ drive.eligibility }}<br>
                      <strong>Deadline:</strong> {{ drive.deadline }}
                  </p>
                  <div class="mt-auto">
                      <button type="button" class="btn btn-info btn-sm w-100 mb-2"
                          @click="openModal(drive)">
                          View Details
                      </button>
                      <!-- Apply Button -->
                      <button v-if="data.student.has_resume"
                          class="btn btn-success btn-sm w-100"
                          @click="applyDrive(drive.id, drive.job_title, drive.company_name)">
                          Apply Now
                      </button>
                      <button v-else class="btn btn-secondary btn-sm w-100" disabled>
                          Upload Resume to Apply
                      </button>
                  </div>
              </div>
          </div>
      </div>
      <div v-if="data.available_drives.length === 0" class="col-12 text-center">
          <p>No available placement drives at the moment.</p>
      </div>
  </div>

  <!-- Details Modal (Vue-controlled, no Bootstrap JS needed) -->
  <div v-if="selectedDrive" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <h5 class="modal-title">{{ selectedDrive.job_title }} at {{ selectedDrive.company_name }}</h5>
                  <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                  <p><strong>Job Description:</strong></p>
                  <p>{{ selectedDrive.job_description }}</p>
                  <hr>
                  <p><strong>Eligibility:</strong> {{ selectedDrive.eligibility }}</p>
                  <p><strong>Deadline:</strong> {{ selectedDrive.deadline }}</p>
                  <p><strong>HR Contact:</strong> {{ selectedDrive.hr_contact }}</p>
              </div>
              <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
                  <button v-if="data.student.has_resume" class="btn btn-success"
                      @click="applyDrive(selectedDrive.id, selectedDrive.job_title, selectedDrive.company_name); closeModal()">
                      Apply Now
                  </button>
              </div>
          </div>
      </div>
  </div>
</div>

<div v-else class="text-center mt-5">
  <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
</div>
</template>
