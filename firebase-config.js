// Pega aquí TU firebaseConfig tal como lo muestra la consola de Firebase (verifica sobre todo apiKey).
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

export const firebaseConfig = {
  apiKey: "AIzaSyAEmETuv2oIVpVMN9_GgXf8k7NpFX762OM",
  authDomain: "inovamagic-98e92.firebaseapp.com",
  projectId: "inovamagic-98e92",
  storageBucket: "inovamagic-98e92.firebasestorage.app",
  messagingSenderId: "849775140376",
  appId: "1:849775140376:web:1ce66fe52eadab529ead6d"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);