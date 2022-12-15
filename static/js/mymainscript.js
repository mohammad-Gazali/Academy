async function updateCart(e) {
    const response = await axios.get(`${location.href}cart/update/${e.dataset.cid}`)
    
    if (typeof response.data !== "string") {
        Swal.fire({
            title: response.data.title,
            text: response.data.message,
            icon: 'success',
            confirmButtonText: response.data.button
        })
    }

    document.getElementById("cart-courses-number").innerHTML = "(" + response.data.items_count + ")"
}


async function deleteFromCart(e) {
    await axios.get(`${location.href}/delete/${e.dataset.cid}`)
    location.reload()
}


async function resetCart() {
    await axios.get(`${location.href}/reset`)
    location.reload()
}