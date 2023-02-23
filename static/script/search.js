function elasticSearch() {
    let input, tableBody, tr, td, footer;
    input = document.getElementById('search');
    quary = input.value.toUpperCase();
    tableBody = document.getElementById('table_body');
    tr = tableBody.getElementsByTagName('tr');
    paginationResult = document.getElementById('pagination-result');
    paginationButtons = document.getElementById('pagination-buttons');

    for (let i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName('td');
        let message = document.getElementById('no-data');
    
        if (td.length > 0) {
            if (td[0].innerHTML.toLocaleUpperCase().indexOf(quary) > -1 ||
                td[1].innerHTML.toLocaleUpperCase().indexOf(quary) > -1 ||
                td[2].innerHTML.toLocaleUpperCase().indexOf(quary) > -1) {
                tr[i].style.display = '';
                paginationResult.style.display = '';
                paginationButtons.style.display = '';
                tableBody.style.paddingBottom = '';
                message.innerHTML = '';
            } else {
                tr[i].style.display = 'none';
                paginationResult.style.display = 'none';
                paginationButtons.style.display = 'none';
            };
        } 
        
        if (td.length == 0) {
            message.innerHTML = 'Product not found!';
            tableBody.style.paddingBottom = '100px';
            paginationResult.style.display = 'none';
            paginationButtons.style.display = 'none';
        };
    };
};