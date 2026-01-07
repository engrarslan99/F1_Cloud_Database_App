'use strict';


import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";


const firebaseConfig = {
    apiKey: "AIzaS*********************************",
    authDomain: "assignment1-451617.firebaseapp.com",
    projectId: "assignment1-451617",
    storageBucket: "assignment1-451617.firebasestorage.app",
    messagingSenderId: "392918732000",
    appId: "1:392918732000:web:c5f91c4b858ec61f22d485"
  };

  window.addEventListener("load", function() {
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    updateUI(this.document.cookie);
    console.log("hello world load");


    document.getElementById('sign-up').addEventListener('click', function(){
        const email = document.getElementById("email").value
        const password = document.getElementById("password").value

        createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {

            const user = userCredential.user;


            user.getIdToken().then((token) => {
                document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                window.location = "/";
            })

        })
        .catch((error) => {
            
            console.log(error.code + error.message);
        })
    });


    document.getElementById("login").addEventListener('click', function(){
        const email = document.getElementById("email").value
        const password = document.getElementById("password").value

        signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {

            const user = userCredential.user;
            console.log("logged in");


            user.getIdToken().then((token) => {
                document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                window.location = "/";
            })


        })
        .catch((error) => {

            console.log(error.code + error.message);
        })
    });


    document.getElementById("sign-out").addEventListener('click', function(){
        signOut(auth)
        .then((output) => {

            document.cookie = "token=;path=/;SameSite=Strict";
            window.location = "/";
        })

    });
  }); 

function updateUI(cookie){
    var token = parseCookieToken(cookie);


    if(token.length > 0){
        document.getElementById("login-box").hidden = true;
        document.getElementById("sign-out").hidden = false;
    } else {
        document.getElementById("login-box").hidden = false;
        document.getElementById("sign-out").hidden = true;
    }
};


function parseCookieToken(cookie){

    var strings = cookie.split(';');


    for (let i = 0; i<strings.length; i++){

        var temp = strings[i].split('=');
        if(temp[0] == "token")
            return temp[1];
    }


    return"";

};
