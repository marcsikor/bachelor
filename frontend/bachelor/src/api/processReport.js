import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const approveReport = async (doc_id, uid, this_paymentName) => {
    try {
        const response = await axios.post(`${BASE_URL}/approve-report`, {
            docId: doc_id,
            userUid: uid,
            paymentName: this_paymentName
        });
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error: ", error.message);
        return "failure";
    }
};

export const rejectReport = async (doc_id, uid, this_paymentName) => {
    try {
        const response = await axios.post(`${BASE_URL}/reject-report`, {
            docId: doc_id,
            userUid: uid,
            paymentName: this_paymentName
        });
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error: ", error.message);
        return "failure";
    }
};

export const payoutReport = async (doc_id, uid, this_paymentName) => {
    try {
        const response = await axios.post(`${BASE_URL}/payout-report`, {
            docId: doc_id,
            userUid: uid,
            paymentName: this_paymentName
        });
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error: ", error.message);
        return "failure";
    }
};