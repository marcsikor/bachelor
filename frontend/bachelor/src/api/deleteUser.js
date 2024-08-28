import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const deleteUser = async (doc_id, this_email) => {
    try {
        const response = await axios.post(`${BASE_URL}/delete-user`, {
            docId: doc_id,
            email: this_email
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