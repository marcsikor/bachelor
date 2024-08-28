import { signOut } from "firebase/auth"; 
import { auth } from "./firebaseCredentials";

export const firebaseLogout = async () => {
  try {
    await signOut(auth);
    return "success"
  } catch (error) {
    console.error("Error logging out: ", error.message);
    return "failure"
  }
};