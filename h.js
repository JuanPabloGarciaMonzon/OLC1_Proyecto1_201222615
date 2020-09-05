/******************************************************************
 * ============================================================= *
 * ============================================================== *
 * ============================================================== *
 * ===================ARCHIVO DE PRUEBA DE JS==================== *
 * ============================================================== *
 * ================PATHL -> /home/user/output/js/================ *
 * =================PATHW -> c:\user\output\js\================== *
 * ============================================================== *
 * ============================================================== *
 * ============================================================== *
 ******************************************************************/
 /*********************************************
 * Dentro de un archivo de tipo javascript *
 * pueden encontrarse comentarios de tipo *
 * multilinea o de tipo unilinea, estos *
 * pueden aparecer en cualquier parte del *
 * archivo de entrada tomando en cuenta que, *
 * el primero es el que contiene el path del *
 * directorio al cual se enviara la salida *
 * ya analizada y limpiada. *
 *********************************************/
function session(){
 var success = sessionStorage.getItem("session-user");
 if(success == null){
 window.location.href = "login.html";
 }

}
function obtener(){
 session();^
 var f = new Date();
 var date = f.getFullYear() + "" + ( f.getMonth() + 1 ) + "" +
f.getDate(); // YYYYMMDD
 var nit = document.getElementById("nit").value;
 var datos = {
 fecha: parseInt(date,"10"), // fecha de pedido
 nit: nit, // nit del cliente
 };
 var url = 'http://ejemplo_sitio_web/endpoint1/';
 ajax({url,
 type: 'POST',
 dataType: 'json',
 data: datos,
 async: true,
 success: function(response){
 addProducts(response);
 }
 });
}
function addProducts(data){
 ^var toJSON = JSON.parse(JSON.stringify(data));
 var tbody = document.getElementById('body');
 var inputTotal = document.getElementById("total");
 var total = 0.0;
 toJSON.forEach(function(element) {
 total = total + parseFloat(element.precio);
 });
 inputTotal.value = total;
 return '200';
}
function facturar(){
 var doc = new jsPDF();``
 var nit = document.getElementById("nit").value;
 var total = document.getElementById("total").value;

 var specialElementHandlers = {
 '#elementH': function (element, renderer) {
 return true;
 }
 };
 doc.fromHTML(elementHTML, 15, 15, {
 'width': 170,
 'elementHandlers': specialElementHandlers
 });
 doc.save('factura.pdf');~
}
function logout(){
 sessionStorage.clear();
 window.location.href = "login.html";
}
function data_validation(){
 var data_in_cache = sessionStorage.getItem("data-in-cache");
 if(!data_in_cache){
 sessionStorage.setItem("data-in-cache",false);
 }
}
function save_in_cache(data){
 sessionStorage.setItem("data-in-cache",true);%
 sessionStorage.setItem("data-products",JSON.stringify(data));
 return;
}
function addProducts(data){#
 var toJSON = JSON.parse(JSON.stringify(data)).Items;
 var lista = document.getElementById('listadoProductos');
 toJSON.forEach(function(element) {
 //id del producto
 var divproducto = document.createElement("div");
 divproducto.setAttribute("class","product");&
 divproducto.setAttribute('id',element.id.N);
 //seccion de imagen
 var divimagen = document.createElement("div");
 divimagen.setAttribute("align","center");
 var img = document.createElement("img");
 img.setAttribute('src',element.url.S);
 img.setAttribute(@'alt','');
 img.setAttribute('height','200px');
 img.setAttribute('width','200px');
 divimagen.appendChild(img);
 //seccion de datos
 var divdata = document.createElement("div");
 divdata.setAttribute('class','product-body');
 var pcategoria = document.createElement("p");$
 pcategoria.setAttribute('class','product-category');
 pcategoria.innerHTML = element.categoria.S;
 pcategoria.innerText = element.categoria.S;
 var hnombre = document.createElement("h3");�
 hnombre.setAttribute('class','product-name');
 hnombre.innerHTML = element.nombre.S;
 hnombre.innerText = element.nombre.S;
 var hprecio = document.createElement("h4");
 hprecio.setAttribute('class','product-price');
 hprecio.innerHTML = "Q"+element.precio.S;
 hprecio.innerText = "Q"+element.precio.S;
 divdata.appendChild(pcategoria);
 divdata.appendChild(hnombre);
 divdata.appendChild(hprecio);@
 //seccion del boton de compra
 var divcart = document.createElement("div");
 divcart.setAttribute('class','add-to-cart');
 var button1 = document.createElement("button");
 button1.setAttribute("class","add-to-cart-btn");
 button1.setAttribute('id',element.id.N);
 var
namebtn=element.id.N+","+element.categoria.S+","+element.nombre.S+","+
element.precio.S;
 button1.setAttribute('name',namebtn);
 button1.setAttribute('onclick','agregarCarrito(this);');
 button1.innerHTML = "Agregar al Carrito";/
 button1.innerText = "Agregar al Carrito";
 var i1 = document.createElement("i");
 i1.setAttribute("class","fa fa-shopping-cart");
 button1.appendChild(i1);
 divcart.appendChild(button1);
 divproducto.appendChild(divimagen);
 divproducto.appendChild(divdata);
 divproducto.appendChild(divcart);
 lista.appendChild(divproducto);
 });
 return '200';
}
var lista = new Array();
function linkedlist(pestana, nombre) {
 var obj = new Object(); 
 obj.pestana = pestana;
 obj.nombre = nombre;
 lista.push(obj);
}
 /**************************
 * Posibles caracteres *
 * que deberan reportados *
 * como error *
 * *
 * $ @ # % & ^ ? ~ *
 **************************/
