<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AlertMessage from '@/components/AlertMessage.vue'

const route = useRoute()
const router = useRouter()
const driveId = route.params.id
const form = ref({ job_title: '', job_description: '', eligibility: '', deadline: '' })
const alert = ref({ message: '', category: '' })

onMounted(async () => {
  const res = await fetch(`/company/drives/edit/${driveId}`, { credentials: 'include' })
  if (res.ok) {
    const data = await res.json()
    form.value = {
      job_title: data.job_title,
      job_description: data.job_description,
      eligibility: data.eligibility,
      deadline: data.deadline   // already formatted as 'YYYY-MM-DDTHH:MM'
    }
  }
})

async function handleSubmit() {
  alert.value = { message: '', category: '' }
  const res = await fetch(`/company/drives/edit/${driveId}`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  const data = await res.json()
  if (res.ok) {
    alert.value = { message: data.message, category: 'success' }
    setTimeout(() => router.push('/company/dashboard'), 1500)
  } else {
    alert.value = { message: data.error, category: 'danger' }
  }
}
</script>

<template>
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow-sm">
            <div class="card-body">
                <h3 class="card-title text-center mb-4">Edit Placement Drive</h3>

                <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

                <form @submit.prevent="handleSubmit">
                    <div class="mb-3">
                        <label for="job_title" class="form-label">Job Title</label>
                        <input type="text" class="form-control" id="job_title" v-model="form.job_title" required>
                    </div>
                    <div class="mb-3">
                        <label for="job_description" class="form-label">Job Description</label>
                        <textarea class="form-control" id="job_description" v-model="form.job_description" rows="4" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="eligibility" class="form-label">Eligibility Criteria</label>
                        <input type="text" class="form-control" id="eligibility" v-model="form.eligibility" required>
                    </div>
                    <div class="mb-3">
                        <label for="deadline" class="form-label">Application Deadline</label>
                        <input type="datetime-local" class="form-control" id="deadline" v-model="form.deadline" required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Update Drive</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>
