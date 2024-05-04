/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

window.addEventListener('DOMContentLoaded', function () {
    // Edit Product Modal
    const editProductModal = new bootstrap.Modal(document.getElementById('editProductModal'));
    const editProductForm = document.getElementById('editProductForm');
    const editProductName = document.getElementById('editProductName');
    const editProductDescription = document.getElementById('editProductDescription');
    const editProductId = document.getElementById('editProductId');

    // Open Edit Product Modal
    function openEditModal(id, name, description) {
      editProductId.value = id;
      editProductName.value = name;
      editProductDescription.value = description;
      editProductModal.show();
    }

    // Example: Open edit modal when edit button is clicked
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
      button.addEventListener('click', function () {
        const id = this.dataset.id;
        const name = this.dataset.name;
        const description = this.dataset.description;
        openEditModal(id, name, description);
      });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const selectAllCheckbox = document.getElementById('select-all');
    const deleteSelectedButton = document.getElementById('delete-selected');

    selectAllCheckbox.addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('input[name="selected_products"]');
        checkboxes.forEach((checkbox) => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    deleteSelectedButton.addEventListener('click', function () {
        const selectedProducts = document.querySelectorAll('input[name="selected_products"]:checked');
        const productIds = Array.from(selectedProducts).map((checkbox) => checkbox.value);

        fetch('/delete_selected', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_ids: productIds }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    });
});

