<template>
    <form class="m-5 card p-3" @submit.prevent="handleLogin">
      <div class="card-body">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Adres email</label>
        <input type="email" v-model="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" required>
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Hasło</label>
        <input type="password" v-model="password"  class="form-control" id="exampleInputPassword1" required>
      </div>
      <p v-if="LogInfailed">Logowanie nie powiodło się, sprawdź proszę swoje dane logowania</p>
      <div class="row row-cols-lg-2">
              <div class="col text-center">
                <button type="submit" class="btn btn-light btn-lg mt-3 button-size">Zaloguj</button>
              </div>
              <div class="col text-center">
                <RouterLink to="/new-password" class="btn btn-light btn-lg mt-3 button-size">Nie mam hasła</RouterLink>
              </div>
              </div>
            </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { firebaseLogin } from "../firebase/firebaseLogin.js"
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { RouterLink, useRouter } from 'vue-router';

const router = useRouter();
const email = ref(null)
const password = ref(null)
const response = ref(null)
const LogInfailed = ref(false)
const curuser = ref(false)
const useremail = ref(null)

onMounted(() => {
  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/auth.user
    curuser.value = true
    useremail.value = user.email;
    // console.log('inside the nemesis')
    // ...
  } else {
    console.log('no user')
  }
});
});


const handleLogin = async () => {
  try {
    response.value = await firebaseLogin(email.value, password.value);
    if (response.value === 'success'){
      // locaton.reload();
      router.push("/");
      console.log("login successful");
    }
    else{
      LogInfailed.value = true
    }
  } catch (e) {
    console.log(e);
  }
};

</script>