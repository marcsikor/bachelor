<template>
<div class="row d-flex justify-content-center row-cols-auto">
  <div v-for="item in items" class="col d-flex justify-content-center m-3">
    <div class="card text-center" style="width: 18rem;">
      <div class="card-body">
          <h5 class="card-title">{{ item.paymentName }}</h5>
          <!-- <p class="card-title">{{ item.message }}</p> -->
          <!-- <p class="card-text">With supporting text below as a natural lead-in to additional content.</p> -->
          <div class="row row-cols-2">
          <div class="col">
            <RouterLink :to="{ name: 'edit', params: { id : item.id }}" class="btn btn-outline-info">Edytuj</RouterLink>
          </div>
          <div class="col">
            <!-- <a href="#" class="btn btn-outline-danger" @click="deleteItem(item.id)">Usuń</a> -->
          <button type="button" class="btn btn-outline-danger" @click="temp()">uwu</button>
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
import { getReportList } from "../api/getReportList.js"
//import axios from "axios";

const items = ref([]);
const userUID = ref(null);

onMounted(async () => {
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/auth.user
        userUID.value = user.uid;
        // console.log(user.uid)
        items.value = await getReportList(userUID.value)
        // console.log(items.value)
        // console.log(items.value.id)
        // ...
      } else {
        console.error('error: user not logged!')
      }
    });
  });


// const counter = ref(0);
const temp = (() => {
    console.log("bruh")
});


</script>