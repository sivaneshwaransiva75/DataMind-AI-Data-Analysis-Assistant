
document.addEventListener("DOMContentLoaded", function () {

    const dataElement = document.getElementById("explorerData");

    if (!dataElement) return;

    const tableBody = document.getElementById("explorerTableBody");
    const searchInput = document.getElementById("explorerSearch");
    const rowsSelect = document.getElementById("rowsPerPage");
    const recordCount = document.getElementById("recordCount");
    const pageInfo = document.getElementById("pageInfo");
    const currentPageDisplay = document.getElementById("currentPage");
    const previousButton = document.getElementById("previousPage");
    const nextButton = document.getElementById("nextPage");
    const emptyMessage = document.getElementById("explorerEmpty");

    let data;

    try {
        data = JSON.parse(dataElement.textContent);
    } catch (error) {
        console.error("DataMind: Dataset JSON could not be read.", error);
        return;
    }

    const rows = data.rows || [];

    let filteredRows = rows;
    let currentPage = 1;
    let rowsPerPage = 5;

    function displayData() {

        const totalRecords = filteredRows.length;
        const totalPages = Math.max(1, Math.ceil(totalRecords / rowsPerPage));

        if (currentPage > totalPages) {
            currentPage = totalPages;
        }

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        const pageRows = filteredRows.slice(start, end);

        tableBody.replaceChildren();

        pageRows.forEach(function (row, index) {

            const tr = document.createElement("tr");

            const numberCell = document.createElement("td");
            numberCell.textContent = start + index + 1;
            tr.appendChild(numberCell);

            row.forEach(function (value) {

                const td = document.createElement("td");
                td.textContent = value ?? "";
                tr.appendChild(td);

            });

            tableBody.appendChild(tr);

        });

        recordCount.textContent = totalRecords + " records available";

        pageInfo.textContent = "Page " + currentPage + " of " + totalPages;

        currentPageDisplay.textContent = currentPage;

        previousButton.disabled = currentPage === 1;

        nextButton.disabled = currentPage >= totalPages;

        emptyMessage.style.display = totalRecords === 0 ? "block" : "none";

    }

    searchInput.addEventListener("input", function () {

        const keyword = searchInput.value.toLowerCase().trim();

        filteredRows = rows.filter(function (row) {

            return row.some(function (value) {

                return String(value ?? "")
                    .toLowerCase()
                    .includes(keyword);

            });

        });

        currentPage = 1;
        displayData();

    });

    rowsSelect.addEventListener("change", function () {

        rowsPerPage = Number(rowsSelect.value);
        currentPage = 1;

        displayData();

    });

    previousButton.addEventListener("click", function () {

        if (currentPage > 1) {
            currentPage--;
            displayData();
        }

    });

    nextButton.addEventListener("click", function () {

        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);

        if (currentPage < totalPages) {
            currentPage++;
            displayData();
        }

    });

    displayData();

    console.log("DataMind Explorer initialized:", rows.length, "records");

});
