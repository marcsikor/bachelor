<template>
  <form @submit.prevent="handleUpdatingUser" class="card">
    <div class="card-body">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Adres email</label>
        <input type="email" v-model="email" class="form-control" id="exampleInputEmail1" disabled>
      </div>
      <div class="mb-3">
        <label for="username" class="form-label">Imię</label>
        <input type="text" v-model="name" class="form-control" id="username" disabled>
      </div>
      <div class="mb-3">
        <label for="usersurname" class="form-label">Nazwisko</label>
        <input type="text" v-model="surname" class="form-control" id="usersurname" disabled>
      </div>
      <div class="mb-3">
        <label for="function" class="form-label ">Pełniona funkcja</label>
        <select v-model="currentFunction" class="form-select" id="function" required>
          <option v-for="userFunction in userFunctions" :value="userFunction.value">{{ userFunction.value }}</option>
        </select>
      </div>
      <div class="text-center">
      <button type="submit" class="btn btn-light">Zatwierdź</button>
    </div>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getUser } from '../api/getUser.js'
import { updateUserAccess } from '../api/updateUserAccess.js'
import { useRoute } from 'vue-router';

const email = ref(null)
const name = ref("")
const surname = ref("")
const currentFunction = ref(null)
const userFunctions = ref([{ id: 1, value: 'Członek stowarzyszenia' }, { id: 2, value: 'Członek zarządu' }, { id: 3, value: 'Skarbnik' }])
const docId = ref(null)

onMounted(async () => {
    docId.value = useRoute().params.id
    const data = await getUser(docId.value)
    
    email.value = data['email']
    name.value = data['name']
    surname.value = data['surname']
    currentFunction.value = data['position']
});

const handleUpdatingUser = async () => {
  //console.log('handleAddingUser')
  await updateUserAccess(docId.value, email.value, currentFunction.value)
};



</script>