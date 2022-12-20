async function updateCart(e, edition) {
	const response = await axios.get(
		`${ edition === undefined ? location.href : edition }cart/update/${e.dataset.cid}`
	);

	if (typeof response.data !== "string") {
		Swal.fire({
			title: response.data.title,
			text: response.data.message,
			icon: response.data.icon || "success",
			confirmButtonText: response.data.button,
		});
	} else {
		Swal.fire({
			title: response.data.title,
			text: response.data.message,
			icon: response.data.icon,
			confirmButtonText: response.data.button,
		});
	}

	document.getElementById("cart-courses-number").innerHTML =
		"(" + response.data.items_count + ")";
}

async function deleteFromCart(e) {
	await axios.get(`${location.href}/delete/${e.dataset.cid}`);
	location.reload();
}

async function resetCart() {
	await axios.get(`${location.href}/reset`);
	location.reload();
}

//| Payment With Stripe
let stripe, elements;
const stripeSubmit = document.getElementById("stripe-submit");

async function createStripeSession() {
	const form = document.getElementById("form-user-info");
	const formData = new FormData(form);

	stripeSubmit.disabled = true;

	try {
		const response = await axios.post("/checkout/stripe", formData);
		const client_secret = response.data.client_secret;

		const appearance = { theme: "flat" };

		elements = stripe.elements({ appearance, clientSecret: client_secret });

		const paymentElement = elements.create("payment");
		paymentElement.mount("#payment-element");

		document
			.querySelector("#payment-form")
			.addEventListener("submit", _stripeFormSubmit);

		document.getElementById("stripe-card").style.display = "block";

		stripeSubmit.disabled = false;
	} catch (e) {
		console.log(e);
		Swal.fire({
			title: "Error",
			text: e.response.data.message,
			icon: "error",
			confirmButtonText: "Continue",
		});
	}
}

async function _stripeFormSubmit(e) {
	e.preventDefault();
	stripeSubmit.disabled = true;
	const host = window.location.protocol + "//" + window.location.host;
	const { error } = await stripe.confirmPayment({
		elements,
		confirmParams: {
			return_url: `${host}/checkout/complete`,
		},
	});

	if (error.type === "card_error" || error.type === "validation_error") {
		Swal.fire({
			title: "Error",
			text: error.message,
			icon: "error",
			confirmButtonText: "Continue",
		});
	} else {
		Swal.fire({
			title: "Error",
			text: "Sorry, There is Something Wrong With Payment Process",
			icon: "error",
			confirmButtonText: "Continue",
		});
	}
	stripeSubmit.disabled = false;
}

async function _checkStripePaymentStatus() {
	const clientSecret = new URLSearchParams(window.location.search).get(
		"payment_intent_client_secret"
	);
	if (!clientSecret) {
		return;
	}
	const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
	switch (paymentIntent.status) {
		case "succeeded":
			Swal.fire({
				title: "Success",
				text: "Your Checkout Has Successed",
				icon: "success",
				confirmButtonText: "Continue",
			});
			break;
		case "processing":
			Swal.fire({
				title: "Processing",
				text: "Your Checkout Is Under Processing",
				icon: "info",
				confirmButtonText: "Continue",
			});
			break;
		default:
			Swal.fire({
				title: "Error",
				text: "Sorry, There is Something Wrong With Payment Process",
				icon: "error",
				confirmButtonText: "Continue",
			});
			break;
	}
}

async function _stripeInit() {
	const { data } = await axios("/checkout/stripe/config");
	stripe = Stripe(data.public_key, { locale: data.locale });
	_checkStripePaymentStatus();
}

_stripeInit();

//| Language Script
let lanFilters = document.querySelectorAll('.language-input')
let html = document.getElementsByTagName('html')[0]

if (lanFilters[0].checked) {
	html.setAttribute("lang", 'ar')
    html.setAttribute("dir", 'rtl')
    html.dir = 'rtl'
} else {
	html.lang = 'en'
    html.removeAttribute("dir")
}
