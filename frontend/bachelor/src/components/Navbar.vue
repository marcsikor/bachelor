<template>
  <nav  class="navbar navbar-expand-lg sticky-top mb-5 p-0 justify-content-between">
      <button class="navbar-toggler m-2" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse mx-4" id="navbarTogglerDemo02">
        <ul class="navbar-nav justify-content-center">
          <li class="nav-item">
            <RouterLink class="nav-link mx-2" to="/">Strona główna</RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" to="/new">Nowy raport</RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" to="/list">Aktywne zgłoszenia</RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" to="/history">Historia</RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item mx-2">
            <RouterLink v-if='userPosition === "Skarbnik" || userPosition === "Członek zarządu"' class="nav-link" to="/open-reports">Zgłoszenia złożone</RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink v-if='userPosition === "Skarbnik"' class="nav-link" to="/new-user">Nowy użytkownik</RouterLink>
          </li>
           <li class="nav-item mx-2">
            <RouterLink v-if='userPosition === "Skarbnik"' class="nav-link" to="/list-users">Lista użytkowników</RouterLink>
          </li>
          <li class="nav-item mx-2">
            <a class="nav-link" @click="handleLogout" v-if="loggedIn">Wyloguj się</a>
            <RouterLink class="nav-link" to="/login" v-else>Zaloguj się</RouterLink>
          </li>
        </ul>
      </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { getAuth, onAuthStateChanged } from "firebase/auth";  
import { firebaseLogout } from "../firebase/firebaseLogout.js"

const router = useRouter();
const loggedIn = ref(false);
const userEmail = ref("")
const userPosition = ref("")

onMounted(async () => {
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
    if (user) {
      userEmail.value = user.email
      loggedIn.value = true
      const customClaim = await user.getIdTokenResult()
      userPosition.value = customClaim.claims.function
    }
    });
  });

const handleLogout = async () => {
  await firebaseLogout();
  loggedIn.value = false
  userPosition.value = ""
  router.push("/login")
}
</script>

<style>
.navbar {
	background-color: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(3.5px);
}
.nav-link:hover {
	background-color: rgb(255, 255, 255);
	color: rgb(0, 0, 0);
}
.nav-link:focus {
	color: rgb(121, 2, 2);
	font-size: 120%;
}
.nav-link {
	color: rgb(121, 2, 2);
	font-size: 120%;
}
</style>