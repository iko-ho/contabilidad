// static/admin/js/invoice_recalculate.js

window.addEventListener('DOMContentLoaded', (event) => {
    console.log('Iniciando script de facturación...');
    
    // Buscar filas que tengan form-row y has_original
    const invoiceRows = document.querySelectorAll('tr.form-row:not(.empty-form)');
    console.log('Filas de factura encontradas:', invoiceRows.length);
    
    // Mostrar información de cada fila
    invoiceRows.forEach((row, index) => {
        console.log(`Fila ${index + 1}:`, {
            id: row.id,
            classes: row.className,
            content: row.textContent.substring(0, 100) + '...' // Mostrar primeros 100 caracteres
        });
        
        // Aquí puedes acceder a los campos específicos de cada fila
        const description = row.querySelector('.field-description input');
        const quantity = row.querySelector('.field-quantity input');
        const unitPrice = row.querySelector('.field-unit_price input');
        
        if (description && quantity && unitPrice) {
            console.log(`  Descripción: ${description.value}`);
            console.log(`  Cantidad: ${quantity.value}`);
            console.log(`  Precio unitario: ${unitPrice.value}`);
        }
    });
});