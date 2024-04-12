
document.addEventListener("DOMContentLoaded", function () {
    var userIcon = document.getElementById("user-icon");
    var userDetailsPopup = document.createElement("div");
    userDetailsPopup.id = "user-details-popup";
    userDetailsPopup.className = "user-details-popup";

    // Read data attributes
    var username = userIcon.dataset.username;
    var email = userIcon.dataset.email;
    var firstname = userIcon.dataset.firstname;
    var lastname = userIcon.dataset.lastname;

    userDetailsPopup.innerHTML = `<h3>User Details:</h3>
                                  <p>Username: ${username}</p>
                                  <p>Email: ${email}</p>
                                  <p>First Name: ${firstname}</p>
                                  <p>Last Name: ${lastname}</p>`;

    document.body.appendChild(userDetailsPopup);

    userIcon.addEventListener("click", function () {
        userDetailsPopup.style.display = userDetailsPopup.style.display === "none" ? "block" : "none";
    
    });

    window.addEventListener("click", function (event) {
        if (event.target !== userDetailsPopup && !userIcon.contains(event.target)) {
            userDetailsPopup.style.display = "none";
        }
    });
});
