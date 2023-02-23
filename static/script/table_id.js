const table_rows = document.querySelectorAll('.table__row');
const footerPaginationform = document.querySelector('#from');
const footerPaginationto = document.querySelector('#to');
const stockQuantity = document.querySelectorAll('.stock-quantity');


for (let i = 1; i < table_rows.length; i++) {
    let firstChild = table_rows[i].children[0];
    firstChild.innerHTML = i;
};

// let firstProductId = table_rows[1].children[table_rows[1].childElementCount-1].children[0].children[0].getAttribute('id');
// let lastProductId = table_rows[table_rows.length-1].children[table_rows[table_rows.length-1].childElementCount-1].children[0].children[0].getAttribute('id');

// footerPaginationform.innerHTML = firstProductId;
// footerPaginationto.innerHTML = lastProductId;
