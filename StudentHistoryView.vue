<script setup>
import { ref, onMounted } from 'vue'

const applications = ref([])

onMounted(async () => {
  const res = await fetch('/student/history', { credentials: 'include' })
  if (res.ok) applications.value = await res.json()
})
</script>

<template>
<h2 class="mb-3">Application History</h2>

<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Date Applied</th>
            <th>Deadline</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="app in applications" :key="app.id">
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>{{ app.date_applied }}</td>
            <td>{{ app.deadline }}</td>
            <td>
                <span v-if="app.status === 'Applied'" class="badge bg-secondary">Applied</span>
                <span v-else-if="app.status === 'Shortlisted'" class="badge bg-primary">Shortlisted</span>
                <span v-else-if="app.status === 'Selected'" class="badge bg-success">Selected</span>
                <span v-else-if="app.status === 'Rejected'" class="badge bg-danger">Rejected</span>
            </td>
        </tr>
        <tr v-if="applications.length === 0">
            <td colspan="5" class="text-center">No applications history found.</td>
        </tr>
    </tbody>
</table>
</template>
