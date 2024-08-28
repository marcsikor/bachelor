import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const getHistory = async (uid) => {
    try {
        const response = await axios.post(`${BASE_URL}/get-history`, {
            userUid: uid,
        });
        if (response.status === 200) {
            // console.log(response.data)
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error getting report list: ", error.message);
        return "failure";
    }
};