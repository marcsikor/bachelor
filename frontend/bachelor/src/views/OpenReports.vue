<template>
<div class="mb-5">
  <h1 class="text-center card py-2">Wydatki przesłane do potwierdzenia</h1>
  <hr class="text-center">
    <div class="row d-flex justify-content-center row-cols-auto">
      <div v-for="item in items" class="col d-flex justify-content-center m-3">
        <div class="card text-center p-3" style="width: 20rem;">
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
              <button type="button" class="btn btn-light button-size" v-if="!item.approved" @click="handleApproveReport(item.userUid, item.docId, item.paymentName)">Zatwierdź</button>
              <h4 v-if="item.approved" style="color: green;">Zatwierdzono</h4>
              <button type="button" class="btn btn-light button-size" v-if="item.approved" @click="handleRejectReport(item.userUid, item.docId, item.paymentName)">Odrzuć</button>
              <button type="button" class="btn btn-light button-size mt-2" v-if="item.approved && userPosition === 'Skarbnik'" @click="handlePayoutReport(item.userUid, item.docId, item.paymentName)">Wypłać</button>
            </div>
            </div>
      </div>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getPrepReportList } from "../api/getPrepReportList.js";
import { approveReport, rejectReport, payoutReport } from "../api/processReport.js";
import { getAuth, onAuthStateChanged } from "firebase/auth";  

const items = ref([]);
// const userUID = ref(null);
// const email = ref(null);
const userPosition = ref('');

onMounted(async () => {    
    items.value = await getPrepReportList()
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
    if (user) {
      const customClaim = await user.getIdTokenResult()
      userPosition.value = customClaim.claims.function
    }
    });
  });

const handleApproveReport = (async (docId, userUid, paymentName) => {
  await approveReport(userUid, docId, paymentName);
  items.value = await getPrepReportList()
});

const handleRejectReport = (async (docId, userUid, paymentName) => {
    await rejectReport(userUid, docId, paymentName);
    items.value = await getPrepReportList()
});

const handlePayoutReport = (async (docId, userUid, paymentName) => {
    await payoutReport(userUid, docId, paymentName);
    items.value = await getPrepReportList()
});


</script>