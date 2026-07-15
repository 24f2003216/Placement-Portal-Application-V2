<script setup>
import { ref, onMounted } from 'vue'
import AlertMessage from '@/components/AlertMessage.vue'

const student = ref(null)
const nameInput = ref('')
const contactInput = ref('')
const resumeFile = ref(null)
const alert = ref({ message: '', category: '' })

onMounted(async () => {
  const res = await fetch('/student/profile', { credentials: 'include' })
  if (res.ok) {
    student.value = await res.json()
    nameInput.value = student.value.name
    contactInput.value = student.value.contact
  }
})

function onFileChange(e) {
  resumeFile.value = e.target.files[0] || null
}

async function handleSubmit() {
  alert.value = { message: '', category: '' }
  const formData = new FormData()
  formData.append('name', nameInput.value)
  formData.append('contact', contactInput.value)
  if (resumeFile.value) formData.append('resume', resumeFile.value)

  const res = await fetch('/student/profile', {
    method: 'POST',
    credentials: 'include',
    body: formData  // multipart — do NOT set Content-Type manually
  })
  const data = await res.json()
  if (res.ok) {
    alert.value = { message: data.message, category: 'success' }
    // Refresh profile data
    const r2 = await fetch('/student/profile', { credentials: 'include' })
    if (r2.ok) student.value = await r2.json()
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
                <h3 class="card-title text-center mb-4">Update Profile</h3>

                <AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

                <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" v-model="nameInput" required>
                    </div>
                    <div class="mb-3">
                        <label for="contact" class="form-label">Contact / Email</label>
                        <input type="text" class="form-control" id="contact" v-model="contactInput" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label d-block">Current Resume</label>
                        <a v-if="student && student.resume_filename"
                            :href="`/static/uploads/${student.resume_filename}`"
                            target="_blank" class="btn btn-sm btn-info mb-2">View Resume</a>
                        <span v-else class="text-danger">No resume uploaded. You must upload a resume to apply for drives.</span>
                    </div>

                    <div class="mb-3">
                        <label for="resume" class="form-label">Upload New Resume (PDF preferred)</label>
                        <input class="form-control" type="file" id="resume" @change="onFileChange" accept="application/pdf">
                    </div>

                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Update Profile</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>
