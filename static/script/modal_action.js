const deleteButtons = document.querySelectorAll('.link-to-delete');
const deleteModal = document.querySelector('#delete__modal');
const section = document.querySelector('#section');
const deleteStockBtn = document.querySelector('#delete-stock-btn');
const cancelDeleteStockBtn = document.querySelector('#cancel-delete-stock-btn');
const tr = document.querySelectorAll('.table__row')

function deleteAnimationStyle(hide=false) {
    if (hide) {
        deleteModal.style.top = '-100%';
        deleteModal.style.zIndex = '-99';
    } else {
        deleteModal.style.top = '0';
        deleteModal.style.zIndex = '999';
    };
};

for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', function() {
        let index = deleteButtons[i].getAttribute('id');
        deleteAnimationStyle();
        deleteStockBtn.children[0].href = `/history/delete/${index}`;
    });
};

cancelDeleteStockBtn.addEventListener('click', function() {
    deleteAnimationStyle(hide=true);
});
