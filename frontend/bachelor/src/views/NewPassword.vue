<template>
  <div class="card">
    <form class='card-body' @submit.prevent="setPassword">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Adres email</label>
        <input type="email" v-model="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" required>
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Hasło</label>
        <input type="password" v-model="password"  class="form-control" id="exampleInputPassword1" required>
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-light button-size">Utwórz konto</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
// import router from "../router";
import { setNewPassword } from "../api/setNewPassword.js"

const email = ref(null)
const password = ref(null)
const router = useRouter()

const setPassword = async () => {

    // console.log('inside setNewPassword');
    await setNewPassword(email.value, password.value);
    router.push('/login')
};

</script>