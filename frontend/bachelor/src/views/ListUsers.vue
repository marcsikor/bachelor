<template>
<div class="mb-5">
  <h1 class="text-center card py-2">Użytkownicy</h1>
  <hr class="text-center">
  <div class="row d-flex justify-content-center row-cols-auto">
    <div v-for="item in items" class="col d-flex justify-content-center m-3">
      <div class="card text-center" style="width: 18rem;">
        <h5 class="card-title">{{ item.email }}</h5>
        <div class="card-body">
            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item text-start">Imię i nazwisko: {{ item.name }} {{ item.surname }}</li>
              <li class="list-group-item text-start">Stanowisko: {{ item.position }}</li>
            </ul>
            <div class="row row-cols-2">
              <div class="col text-start">
                <RouterLink :to="{ name: 'edit-user', params: { id : item.id }}" class="btn btn-light ms-2"><i class="bi bi-pencil"></i></RouterLink>
              </div>
              <div class="col text-end">
                <button type="button" class="btn btn-light me-2" @click="handleDeleteUser(item.id, item.email)"><i class="bi bi-trash"></i></button>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
</div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import { RouterLink } from 'vue-router';
import { getAuth, onAuthStateChanged } from "firebase/auth";  
import { listUsers } from "../api/listUsers.js"
import { deleteUser } from "../api/deleteUser.js"

const items = ref([]);

onMounted(async () => {
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        items.value = await listUsers()
        console.log(items.value)
      } else {
        console.error('error: user not logged!')
      }
    });
  });

const handleDeleteUser = (async (itemId, email) => {
    await deleteUser(itemId, email);
    items.value = await listUsers();
});



</script>