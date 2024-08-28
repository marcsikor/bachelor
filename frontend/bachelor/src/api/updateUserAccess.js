import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const updateUserAccess = async (doc_id, this_email, this_position) => {
    try {
        const response = await axios.post(`${BASE_URL}/update-user-access`, {
            docId: doc_id,
            email: this_email,
            position: this_position
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