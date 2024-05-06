// Initializing Bootstrap attributes
document.querySelectorAll("th").forEach(function(th){
    th.setAttribute("scope", "col")
})

table = document.querySelector("table")
table.classList.add("table")

thead = document.querySelector("thead")
thead.classList.add("thead-dark")

const tBody = document.getElementsByTagName('tbody')[0]
tBody.querySelectorAll("th").forEach(function(th){
    th.setAttribute("scope", "row")
})


/**
 * Sorts a HTML table.
 * 
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending order 
 */

function sortTableByColumn(table, column, asc=true){
    const dirModifier = asc ? 1 : -1
    const tBody = document.getElementsByTagName('tbody')[0]
    const rows = Array.from(tBody.querySelectorAll("tr")) 

    const regInteger = /^[0-9]*$/
    const regFloat = /^[+-]?\d+(\.\d+)?$/
    const columnValues = Array.from(tBody.rows).map(row => row.cells[column].textContent)
    const columnDataTypeIsNumSet = new Set(columnValues.map(value => (regInteger.test(value)) || regFloat.test(value)))
    const columnDataTypeIsNum = Array.from(columnDataTypeIsNumSet)[0]

    const sortedRows = rows.sort(function(a, b){
        const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim()
        const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim()

        // Ignores all null values
        if (aColText == "N/A") return 1
        if (bColText === "N/A") return -1

        if (columnDataTypeIsNum){
            return (Number(aColText) - Number(bColText)) >= 0 ? (1 * dirModifier) : (-1 * dirModifier)
        }   
        return aColText >= bColText ? (1 * dirModifier) : (-1 * dirModifier)
    })

    changeTableOrder(tBody, sortedRows)
    trackSortedColumn(table, column, asc)
}

function changeTableOrder(tableBody, newRows){
    while (tableBody.firstChild){
        tableBody.removeChild(tableBody.firstChild)
    }
    tableBody.append(...newRows) 
}

function trackSortedColumn(table, column, asc){
    table.querySelectorAll("th").forEach(function(th){
        th.classList.remove("th-sort-asc", "th-sort-desc")
    })
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc)
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc)
}


document.querySelectorAll("th").forEach(function(headerCell){
    headerCell.addEventListener("click", function(){
        const tableElement = headerCell.parentElement.parentElement.parentElement
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell)
        currentIsAscending = headerCell.classList.contains("th-sort-asc")

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending)
    })
})