<template>
    <form class="card" @submit.prevent="handleAddingUser">
    <div class = "card-body">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Adres email</label>
        <input type="email" v-model="email" class="form-control" id="exampleInputEmail1" required>
      </div>
      <div class="mb-3">
        <label for="username" class="form-label">Imię</label>
        <input type="text" v-model="name" class="form-control" id="username">
      </div>
      <div class="mb-3">
        <label for="usersurname" class="form-label">Nazwisko</label>
        <input type="text" v-model="surname" class="form-control" id="usersurname">
      </div>
      <div class="mb-3">
        <label for="function" class="form-label ">Pełniona funkcja</label>
        <select v-model="currentFunction" class="form-select" id="function" required>
          <option v-for="userFunction in userFunctions" :value="userFunction.value">{{ userFunction.value }}</option>
        </select>
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-light button-size">Utwórz nowego użytkownika</button>
      </div>
  </div>
  </form>
</template>

<script setup>
import { ref } from "vue";
//import { app } from "../api/firebaseCredentials.js"
import {createUserAccount} from '../api/createUserAccount.js'
import { RouterLink } from 'vue-router';
//import axios from "axios"; 

const email = ref(null)
const name = ref("")
const surname = ref("")
const currentFunction = ref(null)
const userFunctions = ref([{ id: 1, value: 'Członek stowarzyszenia' }, { id: 2, value: 'Członek zarządu' }, { id: 3, value: 'Skarbnik' }])
//const password = ref(null)


const handleAddingUser = async () => {
  //console.log('handleAddingUser')
  await createUserAccount(email.value,name.value,surname.value,currentFunction.value)
};



</script>