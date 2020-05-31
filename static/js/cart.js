var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function () {
    var productId = this.dataset,product
    var action = this.dataset.action
    console.log('productId', productId, 'action:', action)

    console.log('User:', user)
    sleep(2000);
    if(user === 'AnonymousUser'){
      addCookieItem(productId, action)
    }else{
      updateUserOrder(productId, action)
    }
  })
}

function addCookieItem(productId, action){
  var x = productId.product
  if(action == 'add'){
    if(cart[productId.product] == undefined){
      cart[productId.product] = {'quantity':1}
    }else{
      cart[productId.product]['quantity'] += 1
    }
  }
  if(action == 'remove'){
    cart[productId.product]['quantity'] -= 1

    if(cart[productId.product]['quantity'] <= 0){
      console.log('Remove Item')
      delete cart[productId.product]
    }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
  }




function updateUserOrder(productId, action){
  console.log('logged in as....', user)

  var url = '/update_item/'

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body:JSON.stringify({'productId': productId, 'action':action})
   })
   .then((response) => {
     return response.json();
   })



   .then((data) =>{
     console.log('data:', data)
     location.reload();
   })
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
