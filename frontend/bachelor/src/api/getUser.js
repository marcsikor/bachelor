import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const getUser = async (doc_id) => {
    try {
        const response = await axios.get(`${BASE_URL}/get-user/${doc_id}`)
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