		var firebaseConfig = {
			apiKey: "AIzaSyAY2ai-xYdAassFY4bSQg-IGjayiDIPKD4",
			authDomain: "beemathon.firebaseapp.com",
			projectId: "beemathon",
			storageBucket: "beemathon.appspot.com",
			messagingSenderId: "588525140503",
			appId: "1:588525140503:web:ad1442d1140835a102ba52",
			measurementId: "G-2FCBG4EM97"
		};

		// Initialize Firebase
		firebase.initializeApp(firebaseConfig);
		firebase.analytics();

    // Login variables
    var errorMessage = '';
    var visible = false;
    var errorOccured = false;

    // Date
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); 
    var yyyy = today.getFullYear();
    today = mm + '/' + dd + '/' + yyyy;
    
    // Signup with firebase
    function handleSignup() {

				// Local variables
				let name = document.getElementById('name').value;
				let email = document.getElementById('email').value; 
				let phoneNumber = document.getElementById('phoneNumber').value; 
				let password = document.getElementById('password').value;

        firebase.auth().createUserWithEmailAndPassword(email, password) .then((userCredential) => {
            visible = true;
            errorOccured = false;
            // Change login state
            firebase.auth().onAuthStateChanged((user) => {
                if (user) {
                    // Logged in
									  var base_url = window.location.origin;
                    window.location.href = base_url + "/home" 
                } else {
                    // Logged out
									console.log("bye");
                }
            });

            // Make login persistant 
            firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL)
            .then(() => {
                return firebase.auth().signInWithEmailAndPassword(email, password);
            })
            .catch((error) => {
                // Handle Errors here.
                var errorMessage = error.message;
                console.log(errorMessage);
            });

            // Add user information to firebase 
            var user = firebase.auth().currentUser;
            firebase.database().ref('users/' + user.uid).set({
                   	name: name,
                    phoneNumber: phoneNumber,
                    joiningDate: today
            });
        })
        .catch((error) => {
            visible = true;
            errorOccured = true;
            errorMessage = error.message;
        });
	}
