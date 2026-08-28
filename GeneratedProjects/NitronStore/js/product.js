const API = "http://127.0.0.1:8000/products";


const params = new URLSearchParams(window.location.search);

const productId = params.get("id");


async function loadProduct(){

    try{

        const response = await fetch(
            API + "/" + productId
        );


        const product = await response.json();



        document.getElementById("product-image").innerHTML = `

            <img src="images/${product.image}"
            alt="${product.name}">

        `;



        document.getElementById("name").innerText =
        product.name;



        document.getElementById("price").innerText =
        "$" + product.price;



        document.getElementById("description").innerText =
        product.description;



        document.getElementById("size").innerHTML =
        product.size
        .split(",")
        .map(size =>
            `<option>${size}</option>`
        )
        .join("");



        document.getElementById("color").innerHTML =
        `
        <option>${product.color}</option>
        `;


    }

    catch(error){

        console.log(error);

    }

}



loadProduct();
