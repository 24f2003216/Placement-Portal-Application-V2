<script setup>
import { ref, onMounted } from 'vue'
import AlertMessage from '@/components/AlertMessage.vue'

const drives = ref([])
const alert = ref({ message: '', category: '' })

async function loadDrives() {
  const res = await fetch('/admin/drives', { credentials: 'include' })
  if (res.ok) drives.value = await res.json()
}

async function doAction(url) {
  const res = await fetch(url, { credentials: 'include' })
  const data = await res.json()
  alert.value = { message: data.message || data.error, category: res.ok ? 'success' : 'danger' }
  loadDrives()
}

onMounted(loadDrives)
</script>

<template>
<h2 class="mb-3">Manage Placement Drives</h2>

<AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>Drive ID</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="drive in drives" :key="drive.id">
            <td>{{ drive.id }}</td>
            <td>{{ drive.company_name }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.deadline }}</td>
            <td>
                <span v-if="drive.status === 'Pending'" class="badge bg-warning text-dark">Pending</span>
                <span v-else-if="drive.status === 'Approved'" class="badge bg-success">Approved</span>
                <span v-else-if="drive.status === 'Closed'" class="badge bg-secondary">Closed</span>
            </td>
            <td>
                <template v-if="drive.status === 'Pending'">
                    <button class="btn btn-sm btn-success me-1" @click="doAction(`/admin/drives/approve/${drive.id}`)">Approve</button>
                    <button class="btn btn-sm btn-danger" @click="doAction(`/admin/drives/reject/${drive.id}`)">Reject</button>
                </template>
            </td>
        </tr>
        <tr v-if="drives.length === 0">
            <td colspan="6" class="text-center">No placement drives found.</td>
        </tr>
    </tbody>
</table>
</template>
