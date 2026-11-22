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
    const expenseForm = document.getElementById("common-expense-form")
    const enterButton = document.querySelector("#enter-common")

    button.addEventListener('click', function() {
        button.classList.add("hidden");

        inputs.forEach(input => {
            input.classList.remove("hidden")
        });
        inputs[0].focus();
    });

    enterButton.addEventListener('click', () => {
        const expenseName = document.querySelector('[name="name-common-expense"]').value.trim()
        const expenseAmount = document.querySelector('[name="amount-common-expense"]').value
        
        if (!expenseName || !expenseAmount) {
            return;
        }

        const newButton = document.createElement("button");
        newButton.type = "submit";
        newButton.name = "common-expense";
        newButton.value = expenseAmount;
        newButton.innerText = `${expenseAmount} ${expenseName}`; // text that appears in the button
        newButton.className = "common-expense-class"
        
        document.querySelector('[name="custom-name"]').value = expenseName;
        document.querySelector('[name="custom-amount"]').value = expenseAmount;

        expenseForm.appendChild(newButton)
        
        inputs.forEach(input => {
            input.value = "";
        })

    })
}

function enterCommon() { 
    const enterButton = document.getElementById("enter-common"); 
    
    enterButton.addEventListener("click", async () => { 
        const name = document.querySelector('[name="name-common-expense"]').value.trim(); 
        const amount = Number(document.querySelector('[name="amount-common-expense"]').value);

        console.log(Number.isInteger(amount) ? amount : amount.toFixed(2));
        
        // checks for empty values
        if (!name || !amount) {
            alert("empty name and amount field")
            return;
        }

        try { 
            const response = await fetch("/insert-common", { 
                method: "POST", 
                headers: { "Content-Type": "application/json" }, 
                body: JSON.stringify({
                    name: name,
                    amount: amount
                }) 
            }); 
            
            if (response.ok) { 
                alert("Common expense saved"); 
                window.location.reload();
            } else { 
                alert("something errored"); 
            } 
        } catch (error) { 
            console.error("POST error:", error); 
        } 
    });
}

function deleteCommon() {
    const deleteToggleBtn = document.getElementById("delete-common-btn");
    const expenseForm = document.getElementById("common-expense-form");
    let isDeleteMode = false;

    // 1. Toggle Delete Mode when the "Delete" button is clicked
    deleteToggleBtn.addEventListener("click", () => {
        isDeleteMode = !isDeleteMode;
        deleteToggleBtn.innerText = isDeleteMode ? "Done Deleting" : "Delete";
        deleteToggleBtn.style.backgroundColor = isDeleteMode ? "#ff4d4d" : "";
    });

    // 2. Intercept clicks on the common expense buttons
    expenseForm.addEventListener("click", async (event) => {
        const button = event.target.closest(".common-expense-class");
        
        // Only delete if Delete Mode is turned ON
        if (button && isDeleteMode) {
            event.preventDefault(); // Stops POST /add-common from running

            const expenseName = button.value; // Gets {{ item[0] }}

            // Optional: Send request to backend to delete from DB too
            try {
                const response = await fetch("/delete-common", {
                    method: "DELETE",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: expenseName })
                });

                if (response.ok) {
                    button.remove(); // Removes button from screen
                }
                else {
                    alert("failed to remove button")
                }

            } catch (error) {
                console.error("Failed to delete from DB:", error);
            }
        }
    });
}

loadExpensesByPeriod(); 
getExpensesAllTime();
addCommonExpense();
enterCommon();
deleteCommon();