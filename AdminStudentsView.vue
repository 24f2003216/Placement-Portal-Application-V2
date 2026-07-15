<script setup>
import { ref, onMounted } from 'vue'
import AlertMessage from '@/components/AlertMessage.vue'

const students = ref([])
const search = ref('')
const alert = ref({ message: '', category: '' })

async function loadStudents() {
  const url = search.value ? `/admin/students?search=${encodeURIComponent(search.value)}` : '/admin/students'
  const res = await fetch(url, { credentials: 'include' })
  if (res.ok) students.value = await res.json()
}

async function doAction(url) {
  const res = await fetch(url, { credentials: 'include' })
  const data = await res.json()
  alert.value = { message: data.message || data.error, category: res.ok ? 'success' : 'danger' }
  loadStudents()
}

function confirmDelete(userId) {
  if (confirm('Are you sure?')) doAction(`/admin/students/delete/${userId}`)
}

onMounted(loadStudents)
</script>

<template>
<h2 class="mb-3">Manage Students</h2>

<AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

<form class="d-flex mb-4" @submit.prevent="loadStudents">
    <input class="form-control me-2" type="search" v-model="search" placeholder="Search students by name or contact" aria-label="Search">
    <button class="btn btn-outline-success" type="submit">Search</button>
</form>

<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Contact</th>
            <th>Resume</th>
            <th>Active</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="std in students" :key="std.id">
            <td>{{ std.id }}</td>
            <td>{{ std.name }}</td>
            <td>{{ std.contact }}</td>
            <td>
                <a v-if="std.resume_filename" :href="`/static/uploads/${std.resume_filename}`" target="_blank">View Resume</a>
                <span v-else>Not uploaded</span>
            </td>
            <td>
                <span v-if="std.is_active" class="badge bg-primary">Active</span>
                <span v-else class="badge bg-danger">Blacklisted</span>
            </td>
            <td>
                <button :class="`btn btn-sm btn-${std.is_active ? 'warning' : 'info'} me-1`"
                    @click="doAction(`/admin/students/toggle_status/${std.user_id}`)">
                    {{ std.is_active ? 'Blacklist' : 'Activate' }}
                </button>
                <button class="btn btn-sm btn-danger" @click="confirmDelete(std.user_id)">Delete</button>
            </td>
        </tr>
        <tr v-if="students.length === 0">
            <td colspan="6" class="text-center">No students found.</td>
        </tr>
    </tbody>
</table>
</template>
