<template>
<div class="m-5 card p-3">
  <div class="card-body">
    <h1 class = "text-center">Aplikacja do rozliczeń finansowych</h1>
    <div class="text-center">
    <RouterLink class="btn btn-light btn-lg mt-3 button-size" v-if="!loggedIn" to="/login" id="button-size">Zaloguj</RouterLink>
  </div>
      <h3 v-if="loggedIn" class="mt-4 text-center">Zalogowano jako: {{ userEmail }}</h3>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAuth, onAuthStateChanged } from "firebase/auth";  

const loggedIn = ref(false);
const userEmail = ref(null)

onMounted(async () => {
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
    if (user) {
      userEmail.value = user.email
      loggedIn.value = true
    }
    });
  });

import { RouterLink } from 'vue-router';

</script>