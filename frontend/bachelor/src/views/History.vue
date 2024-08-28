<template>
  <div class="mb-5">
    <h1 class="text-center card py-2">Zgłoszenia wypłacone</h1>
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
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="userPosition === 'Członek zarządu' || userPosition === 'Skarbnik'" class="mb-5">
    <h1 class="text-center card py-2">Zgłoszenia wypłacone innych członków</h1>
    <hr class="text-center">
    <div class="row d-flex justify-content-center row-cols-auto">
      <div v-for="item in itemsGlobal" class="col d-flex justify-content-center m-3">
        <div class="card text-center" style="width: 18rem;">
          <h5 class="card-title">{{ item.paymentName }}</h5>
          <div class="card-body">
              <ul class="list-group list-group-flush mb-3">
                <li class="list-group-item text-start">Od: {{ item.userEmail }}</li>
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
  import { getAuth, onAuthStateChanged } from "firebase/auth";  
  import { getStorage, ref as refStorage, getDownloadURL } from "firebase/storage";
  import { getHistory } from "../api/getReportList.js";
  import { getPrepHistory } from "../api/getPrepReportList.js";

  const items = ref([]);
  const itemsGlobal = ref([]);
  const userUID = ref(null);
  const userPosition = ref('');
  
  const updateItemList = (async () => {
    items.value = await getHistory(userUID.value)
    for (let i = 0; i < items.value.length; i++) {
      if(items.value[i].file != 'null'){
        items.value[i].file = await getDownloadURL(refStorage(getStorage(), items.value[i].file))
      }
    } 
  });

  const updateGlobalItemList = (async () => {
    itemsGlobal.value = await getPrepHistory()
    for (let i = 0; i < itemsGlobal.value.length; i++) {
      if(itemsGlobal.value[i].file != 'null'){
        itemsGlobal.value[i].file = await getDownloadURL(refStorage(getStorage(), items.value[i].file))
      }
    } 
  });
  
  onMounted(async () => {
      await updateItemList();
      const auth = getAuth();
      onAuthStateChanged(auth, async (user) => {
      if (user) {
        const customClaim = await user.getIdTokenResult()
        userPosition.value = customClaim.claims.function
      }
      if (userPosition.value === 'Członek zarządu' || userPosition.value === 'Skarbnik'){
        await updateGlobalItemList();
      }
      });
    });  
  </script>