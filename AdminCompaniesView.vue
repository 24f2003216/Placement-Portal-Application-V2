<script setup>
import { ref, onMounted } from 'vue'
import AlertMessage from '@/components/AlertMessage.vue'

const companies = ref([])
const search = ref('')
const alert = ref({ message: '', category: '' })

async function loadCompanies() {
  const url = search.value ? `/admin/companies?search=${encodeURIComponent(search.value)}` : '/admin/companies'
  const res = await fetch(url, { credentials: 'include' })
  if (res.ok) companies.value = await res.json()
}

async function doAction(url, successMsg) {
  const res = await fetch(url, { credentials: 'include' })
  const data = await res.json()
  alert.value = { message: data.message || data.error, category: res.ok ? 'success' : 'danger' }
  loadCompanies()
}

onMounted(loadCompanies)
</script>

<template>
<h2 class="mb-3">Manage Companies</h2>

<AlertMessage :message="alert.message" :category="alert.category" @dismiss="alert.message = ''" />

<form class="d-flex mb-4" @submit.prevent="loadCompanies">
    <input class="form-control me-2" type="search" v-model="search" placeholder="Search companies by name" aria-label="Search">
    <button class="btn btn-outline-success" type="submit">Search</button>
</form>

<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>HR Contact</th>
            <th>Website</th>
            <th>Status</th>
            <th>Active</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="comp in companies" :key="comp.id">
            <td>{{ comp.id }}</td>
            <td>{{ comp.name }}</td>
            <td>{{ comp.hr_contact }}</td>
            <td>{{ comp.website }}</td>
            <td>
                <span v-if="comp.is_approved" class="badge bg-success">Approved</span>
                <span v-else class="badge bg-warning text-dark">Pending</span>
            </td>
            <td>
                <span v-if="comp.is_active" class="badge bg-primary">Active</span>
                <span v-else class="badge bg-danger">Blacklisted</span>
            </td>
            <td>
                <template v-if="!comp.is_approved">
                    <button class="btn btn-sm btn-success me-1" @click="doAction(`/admin/companies/approve/${comp.user_id}`)">Approve</button>
                    <button class="btn btn-sm btn-danger" @click="doAction(`/admin/companies/reject_or_delete/${comp.user_id}`)">Reject</button>
                </template>
                <template v-else>
                    <button :class="`btn btn-sm btn-${comp.is_active ? 'warning' : 'info'}`"
                        @click="doAction(`/admin/companies/toggle_status/${comp.user_id}`)">
                        {{ comp.is_active ? 'Blacklist' : 'Activate' }}
                    </button>
                </template>
            </td>
        </tr>
        <tr v-if="companies.length === 0">
            <td colspan="7" class="text-center">No companies found.</td>
        </tr>
    </tbody>
</table>
</template>
