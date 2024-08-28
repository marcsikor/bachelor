import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const setNewPassword = async (this_email, this_password) => {
    try {
        //console.log('pls be alive')
        //console.log(this_email + '  ' + this_password)
        const response = await axios.post(`${BASE_URL}/register-user`, {
            email: this_email,
            password: this_password
        });
        if (response.status === 200) {
            console.log("Registered user successfully");
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error saving report: ", error.message);
        return "failure";
    }
};