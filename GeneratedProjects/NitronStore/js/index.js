const API = "http://127.0.0.1:8000/products";

const container = document.getElementById("product-container");


async function loadProducts(){

    try{

        const response = await fetch(API);

        const products = await response.json();


        container.innerHTML = "";


        products.forEach(product => {


            container.innerHTML += `

            <div class="card">


                <div class="product-image">

                    <span class="badge">
                        NEW
                    </span>

                    <img 
                    src="images/${product.image}" 
                    alt="${product.name}">

                </div>



                <div class="product-info">

                    <h3>
                    ${product.name}
                    </h3>


                    <p class="price">
                    $${product.price}
                    </p>


                    <p>
                    ${product.description}
                    </p>


                    <button onclick="openProduct(${product.id})">
                    View Product
                    </button>

                </div>


            </div>

            `;


        });


    }
    catch(error){

        console.log(error);

        container.innerHTML =
        "<p>Cannot connect to NeutronStore server</p>";

    }

}



function openProduct(id){

    window.location.href =
    "product.html?id=" + id;

}


loadProducts();
