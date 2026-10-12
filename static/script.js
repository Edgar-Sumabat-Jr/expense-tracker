function loadExpensesByPeriod() {
    fetch('/expenses/weekly')
        .then(response =>{
            if (!response.ok) throw new Error("HTTP" + response.status)
            return response.json();
        })
        .then(data => {
            document.getElementById("weekly-expenses").textContent = data.total.toFixed(2);
        });

    fetch('/expenses/monthly')
        .then(response =>{
            if (!response.ok) throw new Error("HTTP" + response.status)
            return response.json();
        })
        .then(data => {
            document.getElementById("monthly-expenses").textContent = data.total.toFixed(2);
        });

    fetch('/expenses/yearly')
        .then(response =>{
            if (!response.ok) throw new Error("HTTP" + response.status)
            return response.json();
        })
        .then(data => {
            document.getElementById("yearly-expenses").textContent = data.total.toFixed(2);
        })
}

function getExpensesAllTime() {
    fetch('/total-expenses')
        .then(response => {
            if(!response.ok) throw new Error("HTTP" + response.status)
            return response.json();
        })
        .then(data => {
            document.getElementById("total-expenses").textContent = data.total.toFixed(2);
        })
        .catch(error => {
            console.error("Error fetching total_sum:", error);
            document.getElementById("total-expenses").textContent = "Error loading";
        });
}

function addCommonExpense() {
    const button = document.querySelector("#add-common");
    const inputs = document.querySelectorAll(".common-input");

    button.addEventListener('click', function() {
        button.classList.add("hidden");

        inputs.forEach(input => {
            input.classList.remove("hidden")
        });
        inputs[0].focus();
    });


}

function editCommonExpense() {
    const button = document.getElementById("edit-common");
    const input = document.getElementById("edit-common-input");

    button.addEventListener('click', function() {
        button.classList.add("hidden");
        input.classList.remove("hidden");
        input.focus();
    });
}

function deleteCommonExpense() {
    const button = document.getElementById("delete-common");
    const input = document.getElementById("delete-common-input");

    button.addEventListener('click', function() {
        button.classList.add("hidden");
        input.classList.remove("hidden");
        input.focus();
    });
}

loadExpensesByPeriod();
getExpensesAllTime();
addCommonExpense();
editCommonExpense();
deleteCommonExpense();