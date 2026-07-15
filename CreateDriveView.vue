<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AlertMessage from '@/components/AlertMessage.vue'

const router = useRouter()
const form = ref({ job_title: '', job_description: '', eligibility: '', deadline: '' })
const alert = ref({ message: '', category: '' })

async function handleSubmit() {
  alert.value = { message: '', category: '' }
  const res = await fetch('/company/drives/create', {
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
                <h3 class="card-title text-center mb-4">Post a Placement Drive</h3>

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
                        <input type="text" class="form-control" id="eligibility" v-model="form.eligibility"
                            placeholder="e.g., B.Tech CSE CGPA > 8.0" required>
                    </div>
                    <div class="mb-3">
                        <label for="deadline" class="form-label">Application Deadline</label>
                        <input type="datetime-local" class="form-control" id="deadline" v-model="form.deadline" required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Create Drive (Pending Admin Approval)</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>
