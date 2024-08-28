import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const confirmReport = async (uid, doc_id) => {
    try {
        const response = await axios.post(`${BASE_URL}/confirm-report`, {
            userUid: uid,
            docId: doc_id
        });
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error getting report: ", error.message);
        return "failure";
    }
};

export const revertReport = async (uid, doc_id) => {
    try {
        const response = await axios.post(`${BASE_URL}/revert-report`, {
            userUid: uid,
            docId: doc_id
        });
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error getting report: ", error.message);
        return "failure";
    }
};