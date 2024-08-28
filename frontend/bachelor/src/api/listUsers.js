import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const listUsers = async () => {
    try {
        //console.log('pls be alive')
        //console.log(this_email + '  ' + this_password)
        const response = await axios.get(`${BASE_URL}/list-users`);
        if (response.status === 200) {
            return response.data
            // console.log("Added new user successfully");
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error adding user: ", error.message);
        return "failure";
    }
};