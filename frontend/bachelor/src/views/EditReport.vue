<template>
    <div class="card">
      <div class="card-title text-center mt-4"><h3>Edytuj wydatek</h3></div>
    <div class="card-body">
  
      <form @submit.prevent="handleUpdate" class="mb-4 mx-4">
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
        <div class="my-1 text-center" v-if="previousPaymentType === 'Karta' || previousPaymentType === 'Przelew'">
          <a :href="originalFile" target="_blank" class="btn btn-outline-info" >Obecne potwierdzenie przelewu</a>
        </div>
        <div v-if="currentPaymentType === 'Karta' || currentPaymentType === 'Przelew'" class="mb-3">
          <label for="formFile" class="form-label">Potwierdzenie przelewu</label>
          <input class="form-control" type="file" id="formFile" @change="uploadFile($event)">
        </div>
        <div class="text-center">
          <button type="submit" class="btn btn-outline-success mt-3 px-5 py-3">Zatwierdź</button>
        </div>
      </form>
      </div>
    </div>
  </template>
      
  <script setup>
  import { ref, onMounted } from "vue";
  import { useRoute } from "vue-router";
  import { editReport } from "../api/editReport.js"
  import { getReport } from "../api/getReport.js"
  import { getAuth, onAuthStateChanged } from "firebase/auth";  // have to remove that later
  import { getStorage, ref as refStorage, getDownloadURL  } from "firebase/storage";


  const paymentTypes = ref([ 'Gotówka', 'Karta' ,'Przelew' ])
  const paymentName = ref(null)
  const invNo = ref(null)
  const amount = ref(null)
  const currentPaymentType = ref(null)
  const previousPaymentType = ref(null)
  const userUID = ref(null)
  const docId = ref(null)
  const originalFile = ref(null)
  const file = ref(null)
  const data = ref(null)
  
onMounted(async () => {
    // checking user credentials
    docId.value = useRoute().params.id
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        userUID.value = user.uid;
        data.value = await getReport(userUID.value, docId.value);
        paymentName.value = data.value['paymentName']
        invNo.value = data.value['invoiceNumber']
        amount.value = data.value['amount']
        currentPaymentType.value = data.value['currentPaymentType']
        previousPaymentType.value = data.value['currentPaymentType']
        amount.value = data.value['amount']
        if (data.value['file'] !== "null") {
          // console.log('wazup wit u')
          originalFile.value = await getDownloadURL(refStorage(getStorage(), data.value['file']))
        }
        // console.log(originalFile.value)
        // await axios.get(data.value['file'])
        // console.log(originalFile.value, config = { responseType: 'blob' });

      } else {
        console.error('error: user not logged!')
      }
    });
    // useRoute().params.id // ok
    // console.log(await getReport(useRoute().params.id))
  });


  const handleUpdate = async () => {
    const form = new FormData();
    form.append('userUid', userUID.value)
    form.append('paymentName', paymentName.value)
    form.append('invoiceNumber', invNo.value)
    form.append('amount', amount.value)
    form.append('currentPaymentType', currentPaymentType.value)
    form.append('file', file.value)
    form.append('docId', docId.value)
    
    //await addNewReport(userUID.value, userEmail.value, paymentName.value, invNo.value, amount.value, currentPaymentType.value, file.value)
    await editReport(form)
    location.reload()
  }

  function uploadFile(e){
    file.value = e.target.files[0];
  }
  </script>