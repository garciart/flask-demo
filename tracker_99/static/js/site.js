// Set copyright ending year to current year
let date = new Date();
let fullYear = date.getFullYear();
document.getElementById("currentYear").innerHTML = (fullYear !== 2024 ? "2024 -" : "") + fullYear;

// let assignTable = new DataTable("#data-table", assignTableOptions)

let assignTableOptions = {
    order: [[0, "asc"]],
    responsive: true,
    scrollX: true,
    autoWidth: false,
};

// let filterTable = new DataTable("#filter-table", filterTableOptions)

let filterTableOptions = {
    order: [[0, "asc"]],
    responsive: true,
    scrollX: true,
    autoWidth: false,
    initComplete: function () {
        this.api()
            .columns()
            .every(function () {
                let column = this;

                // Skip the columns by checking the text of the header
                let columnHeader = column.header();
                let columnText = columnHeader.textContent || columnHeader.innerText;
                if (columnText === "Actions") return;

                let title = column.footer().textContent;

                // Create input element
                let input = document.createElement('input');
                input.placeholder = title;
                column.footer().replaceChildren(input);

                // Event listener for user input
                input.addEventListener('keyup', () => {
                    if (column.search() !== this.value) {
                        column.search(input.value).draw();
                    }
                });
            });
    },
};
