<template>
<div class="mb-5">
  <h1 class="text-center card py-2">Wydatki nieprzesłane</h1>
  <hr class="text-center">
  <div class="row d-flex justify-content-center row-cols-auto">
    <div v-for="item in items" class="col d-flex justify-content-center m-3">
      <div class="card text-center" style="width: 18rem;">
        <h5 class="card-title">{{ item.paymentName }}</h5>
        <div class="card-body">
            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item text-start">Nr faktury: {{ item.invoiceNumber }}</li>
              <li class="list-group-item text-start">Kwota: {{ item.amount }}</li>
              <li class="list-group-item text-start" >Sposób płatności: {{ item.currentPaymentType }}
                <a v-if="item.currentPaymentType != 'Gotówka' && item.file != 'null'" :href="item.file" target="_blank">
                  <i class="bi bi-file-earmark"></i>
                </a>
              </li> 
            </ul>
            <div class="row row-cols-2">
            <div class="col text-start">
              <RouterLink :to="{ name: 'edit', params: { id : item.id }}" class="btn btn-light ms-2"><i class="bi bi-pencil"></i></RouterLink>
            </div>
            <div class="col text-end">
            <button type="button" class="btn btn-light me-2" @click="deleteItem(item.id)"><i class="bi bi-trash"></i></button>
            </div>
            </div>
            <div class="row row-cols-1 mt-3">
              <div class="col">
                <button type="button" @click="handleConfirmReport(item.id)" class="btn btn-light">Prześlij do potwierdzenia</button>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
  <h1 class="text-center card py-2">Wydatki przesłane do potwierdzenia</h1>
  <hr class="text-center">
  <div class="row d-flex justify-content-center row-cols-auto">
    <div v-for="item in itemsConfirmed" class="col d-flex justify-content-center m-3">
      <div class="card text-center" style="width: 18rem;">
        <h5 class="card-title">{{ item.paymentName }}</h5>
        <div class="card-body">
            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item text-start">Nr faktury: {{ item.invoiceNumber }}</li>
              <li class="list-group-item text-start">Kwota: {{ item.amount }}</li>
              <li class="list-group-item text-start" >Sposób płatności: {{ item.currentPaymentType }}
                <a v-if="item.currentPaymentType != 'Gotówka' && item.file != 'null'" :href="item.file" target="_blank">
                  <i class="bi bi-file-earmark"></i>
                </a>
              </li> 
            </ul>
          </div>
          <div class="row row-cols-1 my-3">
            <div class="col">
              <button type="button" @click="handleRevertReport(item.id)" class="btn btn-light">Anuluj przesyłanie</button>
            </div>
          </div>
      </div>
    </div>
  </div>
  <h1 class="text-center card py-2">Wydatki potwierdzone oczekujące na wypłacenie</h1>
  <hr class="text-center">
  <div class="row d-flex justify-content-center row-cols-auto">
    <div v-for="item in itemsApproved" class="col d-flex justify-content-center m-3">
      <div class="card text-center" style="width: 18rem;">
        <h5 class="card-title">{{ item.paymentName }}</h5>
        <div class="card-body">
            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item text-start">Nr faktury: {{ item.invoiceNumber }}</li>
              <li class="list-group-item text-start">Kwota: {{ item.amount }}</li>
              <li class="list-group-item text-start" >Sposób płatności: {{ item.currentPaymentType }}
                <a v-if="item.currentPaymentType != 'Gotówka' && item.file != 'null'" :href="item.file" target="_blank">
                  <i class="bi bi-file-earmark"></i>
                </a>
              </li> 
            </ul>
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
import { getReportList, getConfirmedReportList, getApprovedReportList } from "../api/getReportList.js";
import { deleteReport } from "../api/deleteReport.js";
import { confirmReport, revertReport } from "../api/confirmReport.js"
import { getStorage, ref as refStorage, getDownloadURL } from "firebase/storage";
//import axios from "axios";

const items = ref([]);
const itemsConfirmed = ref([]);
const itemsApproved = ref([]);
const userUID = ref(null);

const updateItemList = (async () => {
  items.value = await getReportList(userUID.value)
  itemsConfirmed.value = await getConfirmedReportList(userUID.value)
  itemsApproved.value = await getApprovedReportList(userUID.value)

  for (let i = 0; i < items.value.length; i++) {
    if(items.value[i].file != 'null'){
      items.value[i].file = await getDownloadURL(refStorage(getStorage(), items.value[i].file))
    }
  } 
  for (let i = 0; i < itemsConfirmed.value.length; i++) {
    if(itemsConfirmed.value[i].file != 'null'){
      itemsConfirmed.value[i].file = await getDownloadURL(refStorage(getStorage(), itemsConfirmed.value[i].file))
    }
  } 
  for (let i = 0; i < itemsApproved.value.length; i++) {
    if(itemsApproved.value[i].file != 'null'){
      itemsApproved.value[i].file = await getDownloadURL(refStorage(getStorage(), itemsConfirmed.value[i].file))
    }
  } 
});

onMounted(async () => {
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        userUID.value = user.uid;
        updateItemList();
      } else {
        console.error('error: user not logged!')
      }
    });
  });


// const counter = ref(0);
const deleteItem = (async (itemId) => {
    await deleteReport(userUID.value, itemId);
});

const handleConfirmReport = (async (itemId) => {
    await confirmReport(userUID.value, itemId);
    updateItemList();
});

const handleRevertReport = (async (itemId) => {
    await revertReport(userUID.value, itemId);
    updateItemList();
});

</script>