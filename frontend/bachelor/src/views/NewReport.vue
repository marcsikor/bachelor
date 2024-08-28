<template>
    <div class="card">
      <div class="card-title text-center mt-4"><h3>Dodaj nowy wydatek</h3></div>
    <div class="card-body">
  
      <form @submit.prevent="handleInsert" class="mb-4 mx-4">
        <div class="mb-3">
          <label for="paymentName" class="form-label">Nazwa wydatku</label>
          <input v-model="paymentName" type="text" class="form-control" id="paymentName" required>
        </div>
        <div class="mb-3">
          <label for="invNo" class="form-label">Numer faktury</label>
          <input v-model="invNo" type="text" class="form-control" id="invNo">
        </div>
        <div class="mb-3">
          <label for="amount" class="form-label">Kwota</label>
          <input v-model="amount" type="number" step="0.01" class="form-control" id="amount">
        </div>
        <div class="mb-3">
          <label for="paymentType" class="form-label ">Sposób płatności</label>
          <select v-model="currentPaymentType" class="form-select" aria-label="Default select example" id="paymentType"
            required>
            <!-- <option value="0" disabled selected>Wybierz sposób płatności</option> -->
            <option v-for="paymentType in paymentTypes" :value="paymentType">{{ paymentType }}</option>
          </select>
        </div>
        <div v-if="currentPaymentType === 'Karta' || currentPaymentType === 'Przelew'" class="mb-3">
          <label for="formFile" class="form-label">Potwierdzenie przelewu</label>
          <input class="form-control" type="file" id="formFile" @change="uploadFile($event)">
        </div>
        <div class="text-center">
          <button type="submit" class="btn btn-light mt-3">Zatwierdź</button>
        </div>
      </form>
      </div>
    </div>
  </template>
      
  <script setup>
  import { ref, onMounted } from "vue";
  import { addNewReport } from "../api/insertNewReport.js"
  import { getAuth, onAuthStateChanged } from "firebase/auth";
  import { useRouter } from 'vue-router'

  const router = useRouter();
  const paymentTypes = ref(['Gotówka','Karta','Przelew' ])
  const paymentName = ref(null)
  const invNo = ref(null)
  const amount = ref(0)
  const currentPaymentType = ref(null)
  const userUID = ref(null)
  const file = ref(null)
  
  onMounted(() => {
    const auth = getAuth();
    onAuthStateChanged(auth, (user) => {
    if (user) {
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/auth.user
      userUID.value = user.uid;
      // ...
    } else {
      console.error('error: user not logged!')
    }
    });
  });


  const handleInsert = async () => {
    const form = new FormData();
    form.append('userUid', userUID.value)
    form.append('paymentName', paymentName.value)
    form.append('invoiceNumber', invNo.value)
    form.append('amount', amount.value)
    form.append('currentPaymentType', currentPaymentType.value)
    form.append('file', file.value)
    
    //await addNewReport(userUID.value, userEmail.value, paymentName.value, invNo.value, amount.value, currentPaymentType.value, file.value)
    await addNewReport(form)
    router.push('/list')
  }

  function uploadFile(e){
    file.value = e.target.files[0];
  }
  </script>