const myCart = []

const addToCart = document.querySelectorAll('.add-to-cart');
const mainContent = document.getElementById('main-content')

const handleClick = (e) => {
    console.log(e.target)

    if (e.target.classList.contains('add-to-cart')){
    console.log(e.target.parentElement.parentElement)
    const newShopObjectArray = e.target.parentElement.textContent.split('\n')
    const newShopObject = {name: `${newShopObjectArray[1].trim()}`, price: `${newShopObjectArray[2].trim()}`, img: `${e.target.parentElement.parentElement.firstElementChild.src}`}
    myCart.push(newShopObject)
    console.log(myCart)

    const addedMessage = document.createElement('div')

    addedMessage.innerHTML = `
        <div id='disable'>
        <div id="added-message">
            <p class='heavy'>Added ${newShopObject.name} to your cart.</p>
            <p class='bm5'>${myCart.length < 2 ? 'Purchase one more item to get a free coffee in store!': 'Check out to receive your coupon for a free coffee!'}</p>
            <div class="shop-button continue" id='continue'>Continue Shopping</div>
            <div class="shop-button" id='view-cart'>View My Cart</div>
        </div>
        </div>`
        
    mainContent.appendChild(addedMessage);
    
    const handleViewCartClick = () => {
        let newHTML = []
        myCart.map(item => {
            newHTML.push(
            `<div class="sampleItem">
                <img src=${item.img} class="shop-img"/>
                <p>${item.name}</p>
                <p>${item.price}</p>
                <div>Delete</div>
            </div>`)
        })

        console.log('new', newHTML)

        addedMessage.innerHTML = `
        <div id='disable'>
        <div id="added-message">
            ${newHTML}
            <div class="shop-button continue" id='continue'>Continue Shopping</div>
        </div>
        </div>`
    }

    const viewCart = document.getElementById('view-cart');
    viewCart.addEventListener('click', handleViewCartClick);

    const itemsInCart = document.getElementById('items-in-cart')
    {myCart.length > 0 ? itemsInCart.className = 'items-in-cart' : itemsInCart.className = ''}
    itemsInCart.textContent = `${myCart.length}`
    }

    if (e.target.classList.contains('more-info')){
        archivedInnerHTML = e.target.parentElement.innerHTML
        e.target.parentElement.innerHTML = `
        <h1> description here </h1>`
        console.log(archivedInnerHTML)
    }
    //add toggler here -- two divs, one for name/price, one for info

    if (e.target.classList.contains('continue')){
       e.target.parentElement.parentElement.remove();
    }
}

document.addEventListener('click', handleClick)

