let total = 0;

$.ajax({
    async: false,
    type: "GET",
    url: "/get_net_cart",
    success: function (data) {
        let response = data["net_total"];
        console.log(response);
        $.ajax({
            async: false,
            type: "GET",
            url: "/get_cart_total",
            success: function (data) {
                total = parseFloat(data["net_total"]);
            },
        });
    },
});

let net_price;
net_price = total + 0.18 * total;

let total_segment = document.getElementById("total");

let strongElement = document.createElement("strong");
strongElement.textContent = "Net Total: " + total;

let brElement = document.createElement("br");

let spanElement = document.createElement("span");
spanElement.textContent = "GST: +18%";
spanElement.style.color = "red";

let netSpanElement = document.createElement("span");
netSpanElement.textContent = "Net: " + net_price;

total_segment.appendChild(strongElement);
total_segment.appendChild(brElement);
total_segment.appendChild(spanElement);
total_segment.appendChild(brElement.cloneNode(true));
total_segment.appendChild(netSpanElement);

// Create an instance of the Stripe object with your publishable API key
var stripe = window.Stripe("pk_test_51ITkaOAiU7lRVJ2gsjDLmVJ9JTB9IWT9z2pKMG5agR9y8GvCmlrJmsfbYhfThgXvusU95uFmK1kp90sNl7FAvCCz00BtNZQnK9");
var checkoutButton = document.getElementById("checkout-button");

checkoutButton.addEventListener("click", function () {
    // Create a new Checkout Session using the server-side endpoint you
    fetch("/create-checkout-session", {
        method: "POST",
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            return stripe.redirectToCheckout({sessionId: session.id});
        })
        .then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, you should display the localized error message to your
            // customer using `error.message`.
            if (result.error) {
                console.error("Error:", result.error.message);
            }
        })
        .catch(function (error) {
            console.error("Error:", error);
        });
});
